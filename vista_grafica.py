# vista_grafica.py: interfaz grafica sencilla usando tkinter
import tkinter as tk
from reglas import crear_juego, mover_disco, hay_victoria, minimo_teorico
from solucion import resolver

class VistaHanoi:
    def __init__(self, root, tema):
        self.root = root
        self.tema = tema
        self.n_discos = 3
        self.juego = crear_juego(self.n_discos)
        self.origen_seleccionado = None
        self.resolviendo = False

        self.root.title("Torre de Hanói - Interfaz Gráfica")
        self.root.configure(bg=self.tema["fondo"])
        self.root.resizable(False, False)

        self.crear_componentes()
        self.actualizar_vista()

    def crear_componentes(self):
        # 1. Panel superior: movimientos y avisos
        frame_superior = tk.Frame(self.root, bg=self.tema["fondo"], pady=10)
        frame_superior.pack(fill=tk.X)

        self.lbl_movimientos = tk.Label(
            frame_superior,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg=self.tema["fondo"],
            fg=self.tema["texto"]
        )
        self.lbl_movimientos.pack()

        self.lbl_mensaje = tk.Label(
            frame_superior,
            text="Haz clic en una torre para elegir origen y luego en otra para mover el disco.",
            font=("Segoe UI", 10),
            bg=self.tema["fondo"],
            fg=self.tema["mensaje_normal"],
            wraplength=640
        )
        self.lbl_mensaje.pack(pady=4)

        # 2. Canvas para dibujar torres y discos
        self.ancho_canvas = 660
        self.alto_canvas = 280
        self.pos_x = [130, 330, 530]  # Coordenada X central de cada torre (0, 1, 2)
        self.y_base = 240
        self.y_tope_palo = 70

        self.canvas = tk.Canvas(
            self.root,
            width=self.ancho_canvas,
            height=self.alto_canvas,
            bg=self.tema["canvas_fondo"],
            highlightthickness=1,
            highlightbackground="#D1C7B7"
        )
        self.canvas.pack(padx=20, pady=5)
        self.canvas.bind("<Button-1>", self.al_hacer_clic_canvas)

        # 3. Botones bajo cada torre (accesibles tanto por clic en canvas como por boton)
        frame_torres = tk.Frame(self.root, bg=self.tema["fondo"])
        frame_torres.pack(fill=tk.X, padx=20, pady=5)

        for i, nombre in enumerate(["Torre 1 (Origen)", "Torre 2 (Auxiliar)", "Torre 3 (Destino)"]):
            btn = tk.Button(
                frame_torres,
                text=nombre,
                font=("Segoe UI", 9, "bold"),
                width=18,
                command=lambda idx=i: self.tocar_torre(idx)
            )
            btn.pack(side=tk.LEFT, expand=True, padx=8)

        # 4. Panel inferior de controles (selector de discos, reiniciar, resolver automatico)
        frame_inferior = tk.Frame(self.root, bg=self.tema["fondo"], pady=12)
        frame_inferior.pack(fill=tk.X, padx=20)

        lbl_discos = tk.Label(
            frame_inferior,
            text="Discos:",
            font=("Segoe UI", 10),
            bg=self.tema["fondo"],
            fg=self.tema["texto"]
        )
        lbl_discos.pack(side=tk.LEFT, padx=(5, 5))

        self.spin_discos = tk.Spinbox(
            frame_inferior,
            from_=3,
            to=8,
            width=4,
            font=("Segoe UI", 10),
            justify="center",
            command=self.cambiar_discos
        )
        self.spin_discos.delete(0, "end")
        self.spin_discos.insert(0, str(self.n_discos))
        self.spin_discos.pack(side=tk.LEFT, padx=(0, 15))

        btn_reiniciar = tk.Button(
            frame_inferior,
            text="Reiniciar",
            font=("Segoe UI", 9),
            command=self.reiniciar
        )
        btn_reiniciar.pack(side=tk.LEFT, padx=5)

        btn_resolver = tk.Button(
            frame_inferior,
            text="Resolver automático (Recursión)",
            font=("Segoe UI", 9),
            bg="#2A9D8F",
            fg="white",
            activebackground="#21867A",
            activeforeground="white",
            command=self.resolver_automatico
        )
        btn_resolver.pack(side=tk.RIGHT, padx=5)

    def cambiar_discos(self):
        try:
            nuevo = int(self.spin_discos.get())
            if 3 <= nuevo <= 8:
                self.n_discos = nuevo
                self.reiniciar()
        except ValueError:
            pass

    def reiniciar(self):
        self.resolviendo = False
        self.juego = crear_juego(self.n_discos)
        self.origen_seleccionado = None
        self.lbl_mensaje.config(
            text="Juego reiniciado. Haz clic en una torre para iniciar.",
            fg=self.tema["mensaje_normal"]
        )
        self.actualizar_vista()

    def al_hacer_clic_canvas(self, evento):
        # Determina cual torre fue clickeada segun la posicion horizontal X
        x = evento.x
        if x < 230:
            torre = 0
        elif x < 430:
            torre = 1
        else:
            torre = 2
        self.tocar_torre(torre)

    def tocar_torre(self, torre_idx):
        if self.resolviendo:
            return  # No interrumpir mientras resuelve automaticamente

        if hay_victoria(self.juego):
            self.lbl_mensaje.config(
                text="¡Ya ganaste! Presiona 'Reiniciar' para jugar otra partida.",
                fg=self.tema["mensaje_victoria"]
            )
            return

        if self.origen_seleccionado is None:
            # Seleccionar torre de origen
            if len(self.juego["torres"][torre_idx]) == 0:
                self.lbl_mensaje.config(
                    text=f"La Torre {torre_idx + 1} está vacía, no hay disco que mover.",
                    fg=self.tema["mensaje_error"]
                )
                return
            self.origen_seleccionado = torre_idx
            self.lbl_mensaje.config(
                text=f"Torre {torre_idx + 1} seleccionada como origen. Ahora haz clic en la torre destino.",
                fg=self.tema["mensaje_normal"]
            )
            self.actualizar_vista()
        else:
            # Segundo clic: torre de destino
            origen = self.origen_seleccionado
            destino = torre_idx
            self.origen_seleccionado = None

            if origen == destino:
                self.lbl_mensaje.config(
                    text="Mismo origen y destino: selección cancelada.",
                    fg=self.tema["mensaje_normal"]
                )
                self.actualizar_vista()
                return

            valido, motivo = mover_disco(self.juego, origen, destino)
            if valido:
                if hay_victoria(self.juego):
                    self.lbl_mensaje.config(
                        text=f"{self.tema['victoria']} Ganaste en {self.juego['movimientos']} movimientos (mínimo: {minimo_teorico(self.juego['discos'])}).",
                        fg=self.tema["mensaje_victoria"]
                    )
                else:
                    self.lbl_mensaje.config(
                        text=f"Movimiento exitoso: Torre {origen + 1} -> Torre {destino + 1}",
                        fg=self.tema["mensaje_normal"]
                    )
            else:
                self.lbl_mensaje.config(
                    text=f"Movimiento inválido: {motivo}",
                    fg=self.tema["mensaje_error"]
                )
            self.actualizar_vista()

    def actualizar_vista(self):
        n = self.juego["discos"]
        minimo = minimo_teorico(n)
        self.lbl_movimientos.config(
            text=f"Movimientos: {self.juego['movimientos']}  |  Mínimo teórico: {minimo}"
        )

        self.canvas.delete("all")

        # Dibujar base de madera
        self.canvas.create_rectangle(
            30, self.y_base, self.ancho_canvas - 30, self.y_base + 18,
            fill=self.tema["base"], outline="#3E240F", width=2
        )

        # Dibujar las 3 torres (palos)
        for i, x in enumerate(self.pos_x):
            color_palo = self.tema["palo_activo"] if self.origen_seleccionado == i else self.tema["palo"]
            self.canvas.create_rectangle(
                x - 6, self.y_tope_palo, x + 6, self.y_base,
                fill=color_palo, outline="#4A2F13"
            )

            # Triangulo marcador sobre la torre elegida
            if self.origen_seleccionado == i:
                self.canvas.create_polygon(
                    x, self.y_tope_palo - 8,
                    x - 9, self.y_tope_palo - 20,
                    x + 9, self.y_tope_palo - 20,
                    fill="#E63946", outline="#900C3F"
                )

        # Dibujar discos
        alto_disco = 18
        separacion = 20
        ancho_por_disco = 20

        for torre_idx, pila in enumerate(self.juego["torres"]):
            x_centro = self.pos_x[torre_idx]
            for nivel, disco in enumerate(pila):
                ancho_disco = 36 + disco * ancho_por_disco
                x1 = x_centro - (ancho_disco // 2)
                x2 = x_centro + (ancho_disco // 2)
                y2 = self.y_base - (nivel * separacion)
                y1 = y2 - alto_disco

                # Elevar ligeramente el disco seleccionado para dar sensacion visual de "levantado"
                if self.origen_seleccionado == torre_idx and nivel == len(pila) - 1:
                    y1 -= 14
                    y2 -= 14

                color_disco = self.tema["discos"][(disco - 1) % len(self.tema["discos"])]
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color_disco, outline="#222222", width=1.5
                )
                self.canvas.create_text(
                    x_centro, (y1 + y2) // 2,
                    text=str(disco),
                    fill="white",
                    font=("Segoe UI", 9, "bold")
                )

    def resolver_automatico(self):
        if self.resolviendo:
            return
        self.reiniciar()
        self.resolviendo = True
        self.lbl_mensaje.config(
            text="Resolviendo paso a paso con la función recursiva 'resolver'...",
            fg=self.tema["mensaje_normal"]
        )

        pasos = []
        resolver(self.juego["discos"], 0, 2, 1, pasos)

        def ejecutar_paso(indice):
            if not self.resolviendo:
                return
            if indice < len(pasos):
                origen, destino = pasos[indice]
                mover_disco(self.juego, origen, destino)
                self.lbl_mensaje.config(
                    text=f"Paso {indice + 1}/{len(pasos)}: Moviendo disco de Torre {origen + 1} a Torre {destino + 1}",
                    fg=self.tema["mensaje_normal"]
                )
                self.actualizar_vista()
                # Pausa de 500 ms entre cada movimiento
                self.root.after(500, lambda: ejecutar_paso(indice + 1))
            else:
                self.resolviendo = False
                self.lbl_mensaje.config(
                    text=f"{self.tema['victoria']} Resuelto en el mínimo teórico ({len(pasos)} movimientos).",
                    fg=self.tema["mensaje_victoria"]
                )

        ejecutar_paso(0)
