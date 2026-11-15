# vista_grafica.py: interfaz grafica interactiva con modos dia y noche y arrastrar discos
import tkinter as tk
import math
from reglas import crear_juego, mover_disco, hay_victoria, minimo_teorico
from solucion import resolver
from temas import TEMAS

class VistaHanoi:
    def __init__(self, root, tema):
        self.root = root
        self.clave_tema = tema.get("clave", "navidad_noche")
        self.tema = tema
        self.n_discos = 3
        self.juego = crear_juego(self.n_discos)
        self.origen_seleccionado = None
        self.resolviendo = False
        self.es_pantalla_completa = False

        # Variables de arrastrar y soltar (Drag and Drop)
        self.disco_arrastrado = None
        self.origen_arrastre = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_current_x = 0
        self.drag_current_y = 0
        self.drag_activo = False

        # Configuración de ventana
        self.root.title(self.tema.get("titulo", "Torre de Hanói: Navidad"))
        self.root.configure(bg=self.tema["fondo"])
        self.root.geometry("1060x680")
        self.root.minsize(800, 500)
        self.root.resizable(True, True)

        # Iniciar maximizado en Windows
        try:
            self.root.state("zoomed")
        except:
            pass

        # Atajos de teclado para pantalla completa
        self.root.bind("<F11>", lambda e: self.alternar_pantalla_completa())
        self.root.bind("<Escape>", lambda e: self.salir_pantalla_completa())

        # Dimensiones y coordenadas reactivas
        self.ancho_canvas = 1000
        self.alto_canvas = 480
        self.pos_x = [220, 500, 780]
        self.y_base = 380
        self.y_tope_palo = 120

        # Copos de nieve / estrellas fijos normalizados (entre 0.0 y 1.0)
        self.copos = [
            (0.04, 0.12, 2), (0.08, 0.38, 3), (0.14, 0.22, 2), (0.19, 0.58, 4),
            (0.25, 0.14, 3), (0.29, 0.35, 2), (0.35, 0.20, 3), (0.39, 0.50, 4),
            (0.44, 0.28, 2), (0.49, 0.15, 3), (0.54, 0.42, 3), (0.59, 0.22, 2),
            (0.64, 0.60, 4), (0.69, 0.16, 2), (0.73, 0.36, 3), (0.78, 0.25, 2),
            (0.83, 0.54, 3), (0.87, 0.18, 4), (0.92, 0.30, 2), (0.96, 0.48, 3)
        ]

        self.crear_componentes()
        self.actualizar_vista()

    def crear_componentes(self):
        # 1. Panel superior de títulos y HUD
        self.frame_superior = tk.Frame(self.root, bg=self.tema["fondo"], pady=8)
        self.frame_superior.pack(fill=tk.X, padx=20)

        # Título temático principal
        self.lbl_titulo = tk.Label(
            self.frame_superior,
            text=self.tema.get("titulo", "Torre de Hanói: Navidad"),
            font=("Segoe UI", 16, "bold"),
            bg=self.tema["fondo"],
            fg=self.tema["texto"]
        )
        self.lbl_titulo.pack(pady=(0, 4))

        # HUD de Movimientos, Mínimo y Estado
        self.frame_hud = tk.Frame(self.frame_superior, bg=self.tema["fondo"])
        self.frame_hud.pack(fill=tk.X)

        self.lbl_movimientos = tk.Label(
            self.frame_hud,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg=self.tema["fondo"],
            fg=self.tema["texto_hud"]
        )
        self.lbl_movimientos.pack(side=tk.LEFT, padx=10)

        self.lbl_mensaje = tk.Label(
            self.frame_hud,
            text="Arrastra los discos entre torres o haz clic para mover.",
            font=("Segoe UI", 11, "bold"),
            bg=self.tema["fondo"],
            fg=self.tema["mensaje_normal"],
            wraplength=600
        )
        self.lbl_mensaje.pack(side=tk.LEFT, expand=True, padx=10)

        # Controles rápidos de pantalla y discos
        frame_hud_derecha = tk.Frame(self.frame_hud, bg=self.tema["fondo"])
        frame_hud_derecha.pack(side=tk.RIGHT, padx=10)

        lbl_discos = tk.Label(
            frame_hud_derecha,
            text="Discos:",
            font=("Segoe UI", 11, "bold"),
            bg=self.tema["fondo"],
            fg=self.tema["texto_hud"]
        )
        lbl_discos.pack(side=tk.LEFT, padx=(5, 5))

        self.spin_discos = tk.Spinbox(
            frame_hud_derecha,
            from_=3,
            to=8,
            width=3,
            font=("Segoe UI", 11, "bold"),
            justify="center",
            command=self.cambiar_discos
        )
        self.spin_discos.delete(0, "end")
        self.spin_discos.insert(0, str(self.n_discos))
        self.spin_discos.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_fullscreen = tk.Button(
            frame_hud_derecha,
            text="⛶ Pantalla Completa (F11)",
            font=("Segoe UI", 9, "bold"),
            bg="#374151",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            relief="flat",
            padx=8,
            pady=3,
            command=self.alternar_pantalla_completa
        )
        self.btn_fullscreen.pack(side=tk.LEFT)

        # 2. Canvas interactivo central
        self.canvas = tk.Canvas(
            self.root,
            bg=self.tema["canvas_fondo"],
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # Eventos de ratón
        self.canvas.bind("<ButtonPress-1>", self.al_presionar_raton)
        self.canvas.bind("<B1-Motion>", self.al_arrastrar_raton)
        self.canvas.bind("<ButtonRelease-1>", self.al_soltar_raton)
        self.canvas.bind("<Configure>", self.al_redimensionar)

        # 3. Panel inferior de botones y acciones
        self.frame_inferior = tk.Frame(self.root, bg=self.tema["fondo"], pady=10)
        self.frame_inferior.pack(fill=tk.X, padx=20)

        self.btn_reiniciar = tk.Button(
            self.frame_inferior,
            text="Reiniciar",
            font=("Segoe UI", 11, "bold"),
            bg="#E63946",
            fg="white",
            activebackground="#D62828",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.reiniciar
        )
        self.btn_reiniciar.pack(side=tk.LEFT, padx=10)

        self.btn_resolver = tk.Button(
            self.frame_inferior,
            text="Resolver automático (Recursión)",
            font=("Segoe UI", 11, "bold"),
            bg="#2A9D8F",
            fg="white",
            activebackground="#21867A",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.resolver_automatico
        )
        self.btn_resolver.pack(side=tk.LEFT, padx=10)

        # Botón de alternancia directa entre Día y Noche
        self.btn_tema = tk.Button(
            self.frame_inferior,
            text=self.tema["btn_tema_txt"],
            font=("Segoe UI", 11, "bold"),
            bg=self.tema["btn_tema_bg"],
            fg=self.tema["btn_tema_fg"],
            activebackground="#F3F4F6",
            activeforeground="#111827",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.cambiar_tema
        )
        self.btn_tema.pack(side=tk.LEFT, padx=10)

        lbl_ayuda = tk.Label(
            self.frame_inferior,
            text="Arrastra los discos libremente o haz clic para mover | F11: Pantalla completa",
            font=("Segoe UI", 9, "italic"),
            bg=self.tema["fondo"],
            fg=self.tema["mensaje_normal"]
        )
        lbl_ayuda.pack(side=tk.RIGHT, padx=10)

    def al_redimensionar(self, evento):
        if evento.width > 50 and evento.height > 50:
            self.ancho_canvas = evento.width
            self.alto_canvas = evento.height
            self.y_base = int(self.alto_canvas * 0.76)
            self.y_tope_palo = int(self.alto_canvas * 0.26)
            self.pos_x = [
                int(self.ancho_canvas * 0.22),
                int(self.ancho_canvas * 0.50),
                int(self.ancho_canvas * 0.78)
            ]
            self.actualizar_vista()

    def alternar_pantalla_completa(self):
        self.es_pantalla_completa = not self.es_pantalla_completa
        self.root.attributes("-fullscreen", self.es_pantalla_completa)
        if self.es_pantalla_completa:
            self.btn_fullscreen.config(text="✕ Salir Pantalla Completa (Esc)")
        else:
            self.btn_fullscreen.config(text="⛶ Pantalla Completa (F11)")

    def salir_pantalla_completa(self):
        if self.es_pantalla_completa:
            self.alternar_pantalla_completa()

    def cambiar_discos(self):
        texto = self.spin_discos.get()
        if texto.isdigit():
            valor = int(texto)
            if 3 <= valor <= 8:
                self.n_discos = valor
                self.reiniciar()

    def cambiar_tema(self):
        # Alterna exclusivamente entre los dos temas: Día y Noche
        if self.clave_tema == "navidad_noche":
            self.clave_tema = "navidad_dia"
        else:
            self.clave_tema = "navidad_noche"

        self.tema = TEMAS[self.clave_tema]

        # Cambio visual evidente e inmediato en todos los contenedores
        self.root.configure(bg=self.tema["fondo"])
        self.frame_superior.configure(bg=self.tema["fondo"])
        self.frame_hud.configure(bg=self.tema["fondo"])
        self.frame_inferior.configure(bg=self.tema["fondo"])

        self.lbl_titulo.configure(
            text=self.tema.get("titulo", "Torre de Hanói: Navidad"),
            bg=self.tema["fondo"],
            fg=self.tema["texto"]
        )
        self.lbl_movimientos.configure(
            bg=self.tema["fondo"],
            fg=self.tema["texto_hud"]
        )
        self.lbl_mensaje.configure(
            bg=self.tema["fondo"],
            fg=self.tema["mensaje_normal"]
        )
        self.btn_tema.configure(
            text=self.tema["btn_tema_txt"],
            bg=self.tema["btn_tema_bg"],
            fg=self.tema["btn_tema_fg"]
        )
        self.canvas.configure(bg=self.tema["canvas_fondo"])

        self.actualizar_vista()

    def reiniciar(self):
        self.resolviendo = False
        self.juego = crear_juego(self.n_discos)
        self.origen_seleccionado = None
        self.disco_arrastrado = None
        self.origen_arrastre = None
        self.drag_activo = False
        self.lbl_mensaje.config(
            text="Juego reiniciado. Arrastra los discos o haz clic para iniciar.",
            fg=self.tema["mensaje_normal"]
        )
        self.actualizar_vista()

    # ========================================================
    # GESTIÓN DE EVENTOS DE RATÓN (ARRASTRAR Y SOLTAR + CLIC)
    # ========================================================

    def al_presionar_raton(self, evento):
        if self.resolviendo:
            return

        if hay_victoria(self.juego):
            self.lbl_mensaje.config(
                text="¡Ya ganaste! Presiona 'Reiniciar' para jugar otra partida.",
                fg=self.tema["mensaje_victoria"]
            )
            return

        diferencias = [abs(evento.x - px) for px in self.pos_x]
        torre = diferencias.index(min(diferencias))

        self.drag_start_x = evento.x
        self.drag_start_y = evento.y
        self.drag_current_x = evento.x
        self.drag_current_y = evento.y
        self.drag_activo = False

        if len(self.juego["torres"][torre]) > 0:
            self.origen_arrastre = torre
            self.disco_arrastrado = self.juego["torres"][torre][-1]
        else:
            self.origen_arrastre = torre
            self.disco_arrastrado = None

    def al_arrastrar_raton(self, evento):
        if self.resolviendo or hay_victoria(self.juego):
            return

        if self.disco_arrastrado is not None:
            dx = abs(evento.x - self.drag_start_x)
            dy = abs(evento.y - self.drag_start_y)
            if dx > 6 or dy > 6:
                if not self.drag_activo:
                    self.drag_activo = True
                    self.origen_seleccionado = None

            if self.drag_activo:
                self.drag_current_x = evento.x
                self.drag_current_y = evento.y
                self.canvas.config(cursor="fleur")
                self.actualizar_vista()

    def al_soltar_raton(self, evento):
        self.canvas.config(cursor="hand2")

        if self.resolviendo or hay_victoria(self.juego):
            self.disco_arrastrado = None
            self.drag_activo = False
            return

        diferencias = [abs(evento.x - px) for px in self.pos_x]
        torre_destino = diferencias.index(min(diferencias))

        # Caso 1: Arrastre activo completado
        if self.drag_activo and self.disco_arrastrado is not None:
            origen = self.origen_arrastre
            destino = torre_destino

            self.disco_arrastrado = None
            self.origen_arrastre = None
            self.drag_activo = False

            if origen == destino:
                self.lbl_mensaje.config(
                    text="Mismo origen y destino: movimiento cancelado.",
                    fg=self.tema["mensaje_normal"]
                )
            else:
                valido, motivo = mover_disco(self.juego, origen, destino)
                if valido:
                    if hay_victoria(self.juego):
                        self.lbl_mensaje.config(
                            text=f"{self.tema['victoria']} Movimientos: {self.juego['movimientos']} (Mínimo: {minimo_teorico(self.juego['discos'])}).",
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
            return

        # Caso 2: Clic estático sin arrastre
        self.disco_arrastrado = None
        self.drag_activo = False

        if self.origen_seleccionado is None:
            if len(self.juego["torres"][torre_destino]) == 0:
                self.lbl_mensaje.config(
                    text=f"La Torre {torre_destino + 1} está vacía, no hay disco que mover.",
                    fg=self.tema["mensaje_error"]
                )
                return
            self.origen_seleccionado = torre_destino
            self.lbl_mensaje.config(
                text=f"Torre {torre_destino + 1} seleccionada. Haz clic en la torre destino o arrastra el disco.",
                fg=self.tema["mensaje_normal"]
            )
            self.actualizar_vista()
        else:
            origen = self.origen_seleccionado
            destino = torre_destino
            self.origen_seleccionado = None

            if origen == destino:
                self.lbl_mensaje.config(
                    text="Mismo origen y destino: selección cancelada.",
                    fg=self.tema["mensaje_normal"]
                )
            else:
                valido, motivo = mover_disco(self.juego, origen, destino)
                if valido:
                    if hay_victoria(self.juego):
                        self.lbl_mensaje.config(
                            text=f"{self.tema['victoria']} Movimientos: {self.juego['movimientos']} (Mínimo: {minimo_teorico(self.juego['discos'])}).",
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

    # ========================================================
    # ELEMENTOS VISUALES Y DIBUJO EN CANVAS
    # ========================================================

    def dibujar_luna(self, cx, cy):
        # Luna creciente luminosa para la noche
        self.canvas.create_oval(cx - 30, cy - 30, cx + 30, cy + 30, fill="#0F2038", outline="")
        self.canvas.create_oval(cx - 22, cy - 22, cx + 22, cy + 22, fill="#FEF08A", outline="#FDE047", width=1)
        # Recorte de sombra que forma la silueta de medialuna
        self.canvas.create_oval(cx - 9, cy - 28, cx + 30, cy + 18, fill=self.tema["canvas_fondo"], outline="")

    def dibujar_sol(self, cx, cy):
        # Gran Sol radiante dorado para el día
        num_rayos = 10
        for k in range(num_rayos):
            ang = k * (2 * math.pi / num_rayos)
            rx1 = cx + 24 * math.cos(ang)
            ry1 = cy + 24 * math.sin(ang)
            rx2 = cx + 38 * math.cos(ang)
            ry2 = cy + 38 * math.sin(ang)
            self.canvas.create_line(rx1, ry1, rx2, ry2, fill="#F59E0B", width=3, capstyle=tk.ROUND)
        self.canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill="#FBBF24", outline="#F59E0B", width=2)

    def dibujar_nube(self, cx, cy, escala=1.0):
        # Nube blanca esponjosa de día
        partes = [(-22, 4, 16), (-8, -6, 22), (12, -4, 20), (26, 5, 15)]
        for dx, dy, r in partes:
            r_esc = int(r * escala)
            x = cx + int(dx * escala)
            y = cy + int(dy * escala)
            self.canvas.create_oval(
                x - r_esc, y - r_esc, x + r_esc, y + r_esc,
                fill="#FFFFFF", outline="#E2E8F0", width=1
            )

    def dibujar_estrella(self, cx, cy, radio_externo, radio_interno, color_relleno, color_borde):
        puntos = []
        for i in range(10):
            angulo = -math.pi / 2 + i * (math.pi / 5)
            r = radio_externo if i % 2 == 0 else radio_interno
            px = cx + r * math.cos(angulo)
            py = cy + r * math.sin(angulo)
            puntos.extend([px, py])
        self.canvas.create_polygon(
            puntos,
            fill=color_relleno,
            outline=color_borde,
            width=2
        )

    def dibujar_capsula(self, x1, y1, x2, y2, color, texto):
        radio = max(6, (y2 - y1) // 2)
        puntos = [
            x1 + radio, y1,
            x2 - radio, y1,
            x2, y1,
            x2, y1 + radio,
            x2, y2 - radio,
            x2, y2,
            x2 - radio, y2,
            x1 + radio, y2,
            x1, y2,
            x1, y2 - radio,
            x1, y1 + radio,
            x1, y1
        ]
        self.canvas.create_polygon(
            puntos,
            smooth=True,
            fill=color,
            outline="#1F2937",
            width=2
        )
        self.canvas.create_line(
            x1 + radio + 6, y1 + 3,
            x2 - radio - 6, y1 + 3,
            fill="white",
            width=2
        )
        self.canvas.create_text(
            (x1 + x2) // 2, (y1 + y2) // 2,
            text=str(texto),
            fill="white" if color != "#FEF08A" and color != "#FEF3CD" else "#1F2937",
            font=("Segoe UI", 10, "bold")
        )

    def actualizar_vista(self):
        n = self.juego["discos"]
        minimo = minimo_teorico(n)
        self.lbl_movimientos.config(
            text=f"Movimientos: {self.juego['movimientos']}   |   Mínimo: {minimo}"
        )

        self.canvas.delete("all")

        # 1. Elementos celestes según sea Día o Noche
        if self.tema["cielo_elemento"] == "luna":
            # Noche: Luna creciente en la esquina superior izquierda
            self.dibujar_luna(int(self.ancho_canvas * 0.10), int(self.alto_canvas * 0.16))
            # Estrellas y nieve nocturna
            for rx, ry, tam in self.copos:
                px = int(rx * self.ancho_canvas)
                py = int(ry * self.alto_canvas)
                self.canvas.create_oval(
                    px, py, px + tam, py + tam,
                    fill="#FFFFFF", outline=""
                )
        else:
            # Día: Gran Sol radiante en la esquina superior izquierda
            self.dibujar_sol(int(self.ancho_canvas * 0.10), int(self.alto_canvas * 0.16))
            # Nubes blancas flotando en el cielo diurno
            self.dibujar_nube(int(self.ancho_canvas * 0.40), int(self.alto_canvas * 0.14), escala=1.1)
            self.dibujar_nube(int(self.ancho_canvas * 0.88), int(self.alto_canvas * 0.16), escala=0.9)
            # Copos suaves cayendo con la luz del día
            for rx, ry, tam in self.copos[::2]:
                px = int(rx * self.ancho_canvas)
                py = int(ry * self.alto_canvas)
                self.canvas.create_oval(
                    px, py, px + tam, py + tam,
                    fill="#FFFFFF", outline=""
                )

        # 2. Guirnalda de luces navideñas
        luces = ["#EF4444", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#FFFFFF"]
        num_tramos = 12
        ancho_tramo = self.ancho_canvas / num_tramos
        for i in range(num_tramos):
            x_inicio = i * ancho_tramo
            x_fin = (i + 1) * ancho_tramo
            x_medio = (x_inicio + x_fin) / 2
            y_cable = 22
            y_guatita = 36
            self.canvas.create_line(
                x_inicio, y_cable, x_medio, y_guatita, x_fin, y_cable,
                smooth=True, fill="#1E293B", width=2
            )
            color_foco = luces[i % len(luces)]
            self.canvas.create_oval(
                x_medio - 5, y_guatita - 2, x_medio + 5, y_guatita + 12,
                fill=color_foco, outline="#F8FAFC", width=1
            )

        # 3. Base de nieve (diferente textura entre noche y día)
        puntos_nieve = [
            0, self.y_base + 6,
            self.ancho_canvas * 0.25, self.y_base + 2,
            self.ancho_canvas * 0.50, self.y_base + 6,
            self.ancho_canvas * 0.75, self.y_base + 2,
            self.ancho_canvas, self.y_base + 6,
            self.ancho_canvas, self.alto_canvas,
            0, self.alto_canvas
        ]
        self.canvas.create_polygon(
            puntos_nieve,
            smooth=True,
            fill=self.tema["base"],
            outline=self.tema["base_sombra"],
            width=2
        )

        # 4. Postes de las tres torres
        ancho_palo = 12
        for i, x in enumerate(self.pos_x):
            es_activo = (self.origen_seleccionado == i)
            color_palo = self.tema["palo_activo"] if es_activo else self.tema["palo"]

            self.canvas.create_rectangle(
                x - ancho_palo // 2, self.y_tope_palo,
                x + ancho_palo // 2, self.y_base + 4,
                fill=color_palo, outline="#381D0B", width=1.5
            )

            if es_activo:
                self.canvas.create_polygon(
                    x, self.y_tope_palo - 10,
                    x - 10, self.y_tope_palo - 24,
                    x + 10, self.y_tope_palo - 24,
                    fill="#EF4444", outline="#B91C1C", width=1.5
                )

            nombres = ["1 Origen", "2 Auxiliar", "3 Destino"]
            self.canvas.create_text(
                x, self.y_base + 35,
                text=nombres[i],
                font=("Segoe UI", 12, "bold"),
                fill=self.tema["texto"]
            )

        # 5. Dibujar los discos en cada torre
        alto_disco = min(26, int((self.y_base - self.y_tope_palo) / (self.n_discos + 2.5)))
        separacion = alto_disco + 2
        ancho_maximo = min(260, int(self.ancho_canvas * 0.25))
        ancho_minimo = 64
        paso_ancho = (ancho_maximo - ancho_minimo) / max(1, (self.n_discos - 1))

        for torre_idx, pila in enumerate(self.juego["torres"]):
            x_centro = self.pos_x[torre_idx]
            for nivel, disco in enumerate(pila):
                if self.drag_activo and torre_idx == self.origen_arrastre and nivel == len(pila) - 1:
                    continue

                ancho_disco = ancho_minimo + (disco - 1) * paso_ancho
                x1 = int(x_centro - (ancho_disco / 2))
                x2 = int(x_centro + (ancho_disco / 2))
                y2 = self.y_base - (nivel * separacion)
                y1 = y2 - alto_disco

                if self.origen_seleccionado == torre_idx and nivel == len(pila) - 1:
                    y1 -= 16
                    y2 -= 16

                color_disco = self.tema["discos"][(disco - 1) % len(self.tema["discos"])]
                self.dibujar_capsula(x1, y1, x2, y2, color_disco, disco)

        # 6. Disco flotante mientras se arrastra con ratón (Drag & Drop)
        if self.drag_activo and self.disco_arrastrado is not None:
            ancho_drag = ancho_minimo + (self.disco_arrastrado - 1) * paso_ancho
            x1_drag = int(self.drag_current_x - (ancho_drag / 2))
            x2_drag = int(self.drag_current_x + (ancho_drag / 2))
            y1_drag = int(self.drag_current_y - (alto_disco / 2))
            y2_drag = int(self.drag_current_y + (alto_disco / 2))

            # Sombra proyectada
            self.canvas.create_oval(
                x1_drag + 10, y2_drag + 6, x2_drag - 10, y2_drag + 14,
                fill="#000000", outline=""
            )

            color_drag = self.tema["discos"][(self.disco_arrastrado - 1) % len(self.tema["discos"])]
            self.dibujar_capsula(x1_drag, y1_drag, x2_drag, y2_drag, color_drag, self.disco_arrastrado)

        # 7. Estrella dorada navideña y victoria
        color_estrella = self.tema["estrella"]
        borde_estrella = self.tema["estrella_borde"]
        ganado = hay_victoria(self.juego)

        if ganado:
            altura_arbol = len(self.juego["torres"][2]) * separacion
            y_estrella = self.y_base - altura_arbol - 22
            x_estrella = self.pos_x[2]
            self.dibujar_estrella(x_estrella, y_estrella, 26, 11, color_estrella, borde_estrella)

            titulo_victoria = self.tema.get("victoria_titulo", "¡Felices fiestas!")
            self.canvas.create_text(
                self.ancho_canvas // 2 + 2, 72,
                text=titulo_victoria,
                font=("Segoe UI", 26, "bold"),
                fill="#0F172A"
            )
            self.canvas.create_text(
                self.ancho_canvas // 2, 70,
                text=titulo_victoria,
                font=("Segoe UI", 26, "bold"),
                fill=color_estrella
            )
        else:
            self.dibujar_estrella(self.pos_x[2], self.y_tope_palo - 16, 16, 7, color_estrella, borde_estrella)

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
                self.root.after(450, lambda: ejecutar_paso(indice + 1))
            else:
                self.resolviendo = False
                self.lbl_mensaje.config(
                    text=f"{self.tema['victoria']} Resuelto en el mínimo teórico ({len(pasos)} movimientos).",
                    fg=self.tema["mensaje_victoria"]
                )
                self.actualizar_vista()

        ejecutar_paso(0)
