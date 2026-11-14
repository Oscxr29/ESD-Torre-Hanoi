# Torre de Hanói: resumen y plan del proyecto

Estructura de Datos · Parcial 3 · 10 puntos · Python · equipo de 4 · entrega estimada en la primera semana de diciembre (día por confirmar) · actualizado el 13 de noviembre de 2026

Este documento junta todo lo hablado hasta ahora y se limita a lo que se ha visto en clase (repo ETD, hasta la clase 28). Reemplaza al plan de pygame de la primera versión.

---

## 0. Resumen

### Qué se va a hacer

Un juego de la Torre de Hanói en Python con tres torres (origen, auxiliar y destino) hechas con pilas. Rechaza los movimientos inválidos explicando el motivo, cuenta los movimientos, muestra el mínimo teórico `2^n - 1` y detecta la victoria. Se entrega con código modular y comentado, documento técnico, evidencias de pruebas válidas e inválidas y una defensa con participación individual.

### Estado de las decisiones

| Tema | Quién lo definió | Estado |
|------|------------------|--------|
| Equipo de 4 integrantes | Ustedes | Falta confirmar con el docente, porque Canvas habla de 5 |
| Entrega en la primera semana de diciembre | Ustedes | Día exacto por confirmar. Cierre interno propuesto: sábado 28 de noviembre |
| Límite: solo lo visto en clase | Ustedes | Vigente. El repo ETD llega hasta la clase 28 |
| Interfaz gráfica básica con tema propio | Ustedes | Les interesa. Falta saber si habrá feria o solo defensa |
| Consola completa primero, ventana después | Propuesta | Falta que el equipo la acepte (sección 3) |
| Librería de la ventana | Propuesta | `tkinter` por defecto, `pygame-ce` si alguien la domina (sección 3.3) |
| Solución automática con recursión | Propuesta | Posible desde las clases 27 y 28 (sección 7) |
| Reparto en 4 archivos propios | Propuesta | Sección 9 |
| Preguntas al docente | Pendiente | Sección 13 |

### Qué cambió en esta versión

1. Las clases 27 y 28 (recursividad y pila de llamadas) ya están en el repo. La solución automática deja de ser un extra arriesgado y se puede defender. También da un buen tema para el documento: la recursión usa una pila, igual que las torres.
2. Un proyecto de Hanói de otro equipo (la captura que encontraron) sirve de referencia visual y de estructura. Qué tomar y qué no está en la sección 3.4.
3. La sección 3.3 explica qué es `tkinter` y compara las opciones de librería gráfica.
4. El calendario arranca desde hoy (sección 10), las preguntas al docente están ordenadas (sección 13) y hay un esquema del documento técnico y de la defensa (sección 16) y reglas de Git (sección 17).

### Qué hacer esta semana

1. Una persona crea el repo en GitHub y da permisos a las otras tres.
2. Los cuatro aprueban el contrato de funciones (sección 4) y el reparto (sección 9).
3. Se mandan las preguntas al docente (sección 13).
4. Cada quien revisa su versión de Python y, si va a probar la ventana, que `tkinter` abra una ventana de prueba (en Windows también sirve `py`):

```bash
python --version
python -m tkinter
```

5. Cada quien empieza su archivo. La persona 4 empieza `pruebas.py` contra el contrato, sin esperar al código.

---

## 1. Decisiones principales

| Tema | Decisión | Por qué |
|------|----------|---------|
| Interfaz | Primero consola, completa y obligatoria. Después una ventana básica como segunda vista sobre las mismas reglas (`tkinter` por defecto, ver sección 3.3) | La guía permite consola. `tkinter` viene con Python pero no se ha visto en clase, así que la entrega no puede depender de él. |
| Tema visual | Un tema propio, definido en un diccionario de colores y textos | Cambiar de tema no toca las reglas. Ideas en la sección 3.2. |
| Estructura de datos | Tres pilas (lista de Python con `push` y `pop` como funciones) | Es exactamente lo de las clases 12 a 16. Se puede defender sin trucos. |
| Organización | Varios archivos `.py` con funciones, un archivo por responsabilidad | Lo pide la guía ("archivos modulares y comentados"). |
| Estado del juego | Un diccionario con discos, torres y movimientos | Los diccionarios se vieron en la clase 11. Evita variables globales sueltas. |
| Pruebas | Un `pruebas.py` con `if/else` y `print` que muestra OK o FALLO | No se ha visto `assert` ni `unittest`. Es lo que se puede capturar como evidencia. |
| Manejo de errores | Validar con `if`, sin `try/except` | `try/except` no aparece en el repo. |
| Solución automática | Función recursiva `resolver`, como extra defendible | La recursión y la pila de llamadas se vieron en las clases 27 y 28. |

---

## 2. Qué se ha visto en clase (según el repo ETD)

Revisé la estructura de `computo1`, `computo2` y `computo3` y leí los archivos de pilas, colas, el sistema del banco y los de recursividad para ver el estilo. Son 40 archivos `.py` y ningún `.env`, `.gitignore` ni README. Última revisión: 13 de noviembre, hasta la clase 28.

| Tema | Dónde aparece | Cómo lo usamos |
|------|---------------|----------------|
| Variables, `input`, números | `computo1/clase3` | Pedir discos y torres, calcular `2 ** n - 1` |
| Strings | `Cuaderno de Trabajo1/ejercicios_String.py` | Dibujar discos con `"#" * k`, `.center()` y f-strings |
| Listas | `clase4/listas.py` | Base de cada torre |
| Tuplas | `clase9/tuplas.py` | Devolver `(valido, motivo)` desde la validación |
| Diccionarios | `clase11/diccionario.py` | Estado del juego |
| Condicionales | `computo2/clase14` | Todas las reglas |
| Funciones | `clase15/funciones.py` | Todo el código va en funciones |
| Pilas | `clase12/pila.py`, `clase16/funcionesPila.py` | Las tres torres |
| Menú con `while True` | `clase17/SistemaDeUnBanco.py` | Bucle principal del juego |
| Clases (`Nodo`, `Grafo`) | `clase18` en adelante | Solo si el equipo las quiere. No hacen falta. |
| Recursión (caso base y llamada recursiva) | `clase27/Recursividad.py` (factorial) y `clase20/arbolBST.py` | Solución automática: `resolver` |
| Pila de llamadas y comparación con iteración | `clase28/CallStack.py` y `clase28/iteraciones.py` | Explicar en el documento por qué la recursión usa una pila |

### Lo que no se ha visto y evitamos

| Evitar | Alternativa |
|--------|-------------|
| `pygame` y `pygame-ce` | Dibujo en consola y ventana básica con `tkinter`. `pygame-ce` solo si el equipo lo decide antes del 21 de noviembre (sección 3.3) |
| `pytest`, `assert`, `unittest` | `pruebas.py` con `if/else` |
| `try/except` | Validar con `if` y `.isdigit()` |
| `if __name__ == "__main__":` | Llamar `jugar()` al final de `main.py` |
| Type hints, `dataclass` | Nada, el estilo de clase no los usa |
| Generadores (`yield`) | Una función normal que llena una lista de pasos |

Hay una cosa nueva inevitable: `from archivo import funcion`. La guía pide archivos modulares y el repo no tiene ningún `import` todavía. Es una línea por archivo. Conviene preguntarle al docente si hay problema (sección 13) y, mientras tanto, explicarlo en 10 minutos al equipo. La segunda cosa nueva es `tkinter`, solo si se hace la ventana (sección 3).

---

## 3. Interfaz: consola primero, ventana básica después

Se construyen dos vistas sobre las mismas reglas. Como `reglas.py` no sabe nada de cómo se muestra el juego, la ventana se puede sumar sin tocar la lógica ni las pruebas.

| | Consola | Ventana básica (`tkinter`) |
|---|---------|----------------------------|
| Visto en clase | Sí | No |
| Instalación | Ninguna | Viene con Python en Windows y macOS. En Linux hace falta el paquete `python3-tk`. |
| Esfuerzo | Poco | Medio |
| Riesgo con la rúbrica | Bajo | Medio: hay que aprender `tkinter` mientras se avanza |
| Para una feria de logros | Se ve simple | Mucho mejor: la gente puede tocarlo |
| En la defensa | Cada quien explica su función | Quien hace la ventana explica cómo un clic llega a `mover_disco` |

Todavía no se sabe si habrá feria o solo defensa, así que la estrategia cubre las dos:

1. La consola se termina completa (reglas, mensajes, contador, pruebas). Eso ya cumple todo lo obligatorio.
2. La ventana avanza en paralelo desde el inicio, con un punto de control: si el 21 de noviembre la consola no está integrada, la ventana se congela hasta que lo esté.
3. La ventana nunca reemplaza a la consola. Si algo falla antes de la entrega, se presenta la consola.

### 3.1 Qué hace la ventana básica

| Elemento | Detalle |
|----------|---------|
| Dibujo | Tres palos y los discos como rectángulos de colores en un `Canvas` |
| Interacción | Clic en una torre para elegir el origen y clic en otra para elegir el destino. La torre elegida se resalta. |
| Datos en pantalla | Movimientos, mínimo teórico y una línea con el último mensaje |
| Rechazos | Se muestra en la ventana el mismo texto que devuelve `validar_movimiento` |
| Controles | Selector de discos (3 a 8), botón Reiniciar y botón para cambiar de tema |
| Victoria | Mensaje con los movimientos hechos y el mínimo |

Funciones previstas en `vista_grafica.py` (solo contrato, sin código todavía):

| Función | Qué hace |
|---------|----------|
| `crear_ventana(juego, tema)` | Crea la ventana, el `Canvas`, las etiquetas y los botones |
| `dibujar(juego, tema)` | Borra y vuelve a dibujar torres y discos a partir de `juego["torres"]` |
| `al_hacer_clic(evento)` | Calcula en qué torre cayó el clic (por la coordenada x) y decide si es origen o destino |
| `intentar_mover(origen, destino)` | Llama a `mover_disco`, muestra el motivo si lo rechaza y revisa `hay_victoria` |
| `reiniciar(n)` | Llama a `crear_juego(n)` y redibuja |

De `tkinter` la persona 3 necesita `Tk()`, `Canvas`, `create_rectangle`, `bind("<Button-1>", ...)`, `Label`, `Button` y `mainloop()`. Con un par de sesiones de práctica alcanza para esto.

Si alguien trabaja en WSL, `tkinter` puede no abrir ventana (en Windows 11 con WSLg suele funcionar, en Windows 10 no). Lo más simple es probar la ventana con el Python de Windows. En la semana 1 todos corren `python -m tkinter` para comprobar que se abre una ventana de prueba.

### 3.2 Temas

Un tema es un diccionario con colores y textos, guardado en `temas.py` (los diccionarios se vieron en la clase 11). Cambiar de tema cambia ese diccionario y nada más.

```python
TEMAS = {
    "clasico": {
        "titulo": "Torre de Hanoi",
        "fondo": "#f4ecd8",
        "palo": "#8b5a2b",
        "base": "#5c3a1a",
        "discos": ["#e63946", "#f4a261", "#e9c46a", "#2a9d8f",
                   "#457b9d", "#6a4c93", "#c77dff", "#8d99ae"],
        "victoria": "Lo lograste"
    },
}
```

Ideas de tema. Todas salen de colores y textos, sin imágenes:

| Tema | Discos | Fondo y palos | Mensaje de victoria |
|------|--------|---------------|---------------------|
| Clásico | Colores de arcoíris | Madera | "Lo lograste" |
| Pupusería | Tonos de maíz y dorado, de la pupusa más pequeña a la más grande | Comal oscuro, palos de madera | "¡Listas las pupusas!" |
| Espacial | Planetas y lunas por tamaño | Azul noche, palos como antenas | "Misión cumplida" |
| Arcade retro | Colores neón | Negro, letra monoespaciada | "YOU WIN" |
| Pastelería | Donas con glaseado de colores | Crema | "¡A comer donas!" |
| Del equipo | Los colores que elijan y el nombre de la universidad | A definir | A definir |

Mi recomendación es Clásico como tema por defecto, porque siempre funciona, y uno propio con botón para alternar. Para una feria, Pupusería llama la atención y es difícil que otro equipo tenga algo igual. Conviene evitar personajes, logos y música de juegos o marcas conocidas. No hacen falta y es mejor que el tema sea del equipo.

### 3.3 Stack gráfico: qué es tkinter y qué otras opciones hay

`tkinter` es la librería estándar de Python para hacer ventanas. Viene incluida con Python: en el instalador de python.org para Windows y macOS ya está marcada, y en Linux hace falta el paquete `python3-tk`. Está construida sobre Tk, un sistema de ventanas que existe desde hace décadas, así que se ve sencilla pero funciona igual en Windows, macOS y Linux.

Lo que cambia respecto a la consola es la forma de pensar el programa. En consola, el código recorre un `while True` y pide datos con `input`. En una ventana, el código dibuja todo y llama a `mainloop()`, que se queda esperando. Cada clic o tecla ejecuta una función que ustedes definieron (un evento). Por eso importa tanto que las reglas no sepan nada de la vista: la ventana solo traduce un clic en `mover_disco(juego, origen, destino)` y vuelve a dibujar.

Ejemplo mínimo, una ventana con un rectángulo que imprime dónde se hace clic:

```python
import tkinter as tk

ventana = tk.Tk()
ventana.title("Prueba de tkinter")

lienzo = tk.Canvas(ventana, width=300, height=200, bg="#f4ecd8")
lienzo.pack()

lienzo.create_rectangle(100, 150, 200, 180, fill="#e63946")  # un disco

def al_clic(evento):
    print("Clic en x =", evento.x, "y =", evento.y)

lienzo.bind("<Button-1>", al_clic)
ventana.mainloop()
```

Piezas de `tkinter` que necesitaría la persona 3:

| Pieza | Para qué |
|-------|----------|
| `Tk()` y `mainloop()` | Crear la ventana y mantenerla abierta |
| `Canvas` con `create_rectangle`, `create_oval` y `create_text` | Dibujar palos, discos y números |
| `bind("<Button-1>", funcion)` | Reaccionar al clic izquierdo. El evento trae `x` y `y` |
| `Label` y `Button` | Mostrar textos (movimientos, mínimo, mensaje de rechazo) y botones (Reiniciar, Resolver, Tema) |
| `Spinbox` o `Scale` | Elegir la cantidad de discos |
| `after(milisegundos, funcion)` | Repetir algo cada cierto tiempo, por ejemplo mover los discos de la solución automática uno por uno. No usar `time.sleep`, porque congela la ventana |
| `tags` y `delete("torres")` | Borrar solo torres y discos antes de redibujar, sin tocar el fondo |

Opciones de librería:

| Opción | Qué es | Instalación | Dificultad | Para este proyecto |
|--------|--------|-------------|------------|--------------------|
| `tkinter` | Ventanas y dibujo, incluida en Python | Ninguna (Linux: `python3-tk`) | Media baja | Recomendada por defecto. No hay nada que instalar en la computadora de la feria |
| `turtle` | Dibujo con una tortuga, incluida en Python y construida sobre `tkinter` | Ninguna | Baja | Sirve para probar, pero hacer clic sobre discos es torpe y se ve infantil |
| `customtkinter` | `tkinter` con botones y colores más modernos | `pip install customtkinter` | Media baja | Mejora los botones, pero el dibujo sigue siendo `Canvas`. Es una dependencia extra que el docente podría no aceptar |
| `pygame` o `pygame-ce` | Librería para juegos: imágenes, escalado, sonido y animación | `pip install pygame-ce` | Media | La mejor opción para parecerse al proyecto de la captura. Usa un `while True` con `pygame.event.get()`, parecido al bucle de la clase 17. Hay que instalarla en cada computadora |
| PyQt o PySide | Entorno de escritorio profesional | `pip install` | Alta | Demasiado para esta entrega |
| Kivy | Aplicaciones táctiles y móviles | `pip install kivy` | Alta | No aporta aquí |
| Web (Flask, HTML y JavaScript) | Juego en el navegador | `pip install flask` | Alta para este curso | Canvas pide Python, y esto sacaría la lógica de Python o complicaría la defensa |

`pygame-ce` es una versión mantenida por la comunidad del mismo proyecto y se importa igual (`import pygame`). No conviene instalar `pygame` y `pygame-ce` a la vez.

Recomendación y regla de decisión:

1. Por defecto, `tkinter`. Es lo que menos riesgo trae: no se instala nada, no hay sorpresas el día de la feria y se explica en la defensa.
2. `pygame-ce` solo si alguien del equipo ya la usó, se compromete con la ventana y los cuatro pueden instalarla. Lo que se gana es escalar imágenes, animaciones suaves y sonido.
3. La decisión se toma antes del 21 de noviembre y no se cambia después. Rehacer la ventana a la mitad cuesta más que cualquier diferencia entre las dos.
4. En cualquier caso, las reglas, la consola y las pruebas no cambian. La ventana solo llama a `mover_disco`, `hay_victoria` y `resolver`. Con `pygame-ce` el archivo se sigue llamando `vista_grafica.py`.

Sobre el aspecto: lo que hace que el proyecto de la captura se vea bien son las imágenes (fondo pixel art, base de madera, botones), no la librería. `tkinter` también muestra imágenes PNG con `PhotoImage`, pero solo puede agrandarlas o reducirlas por factores enteros. Con imágenes de tamaño fijo funciona bien. Si hay que escalarlas a cualquier medida, `pygame-ce` es más cómoda. Si nadie dibuja, el tema se logra solo con rectángulos, óvalos y colores (sección 3.2).

### 3.4 Proyecto de referencia (de otro equipo)

La captura que encontraron muestra un Hanói hecho con `pygame-ce`, con tema espacial en pixel art. Solo vi la captura, no el código, así que no puedo opinar sobre cómo está programado. Esto es lo que se ve:

| Lo que se ve | Qué significa para nosotros |
|--------------|-----------------------------|
| Carpetas `game`, `models`, `ui`, `utils`, `assets` y `docs`, más `main.py`, `README.md` y `.gitignore` | Misma idea que nuestra arquitectura: reglas separadas de la interfaz. Nosotros lo hacemos con archivos sueltos en vez de carpetas |
| `ui/console_ui.py` y `ui/gui.py` | Dos vistas sobre el mismo juego, igual que `vista.py` y `vista_grafica.py` |
| Se ejecuta con `py -m ui.gui` | Es la forma de correr código dentro de carpetas con imports. Funciona, pero agrega una complicación que no se ha visto en clase. Con archivos en la raíz basta `python main_grafico.py` |
| Datos en pantalla: `MIN: 1023`, `DISCOS: 10`, `MOVES: 5` | Son los datos que pide Canvas (mínimo teórico, cantidad de discos y movimientos). 1023 es `2^10 - 1`. Ellos llegan a 10 discos, nosotros pensamos en 3 a 8 y se puede subir |
| Botones `MENU` y `RETRY` | Menú y reiniciar. Conviene tener los dos |
| Fondo espacial, base de madera y discos de colores | Es el nivel 3 del tema Espacial de la sección 3.2 |
| Rama `feature/v2-punto4-hud` y autores en el editor | Trabajan con ramas por tarea (sección 17) |

Qué tomar: la separación consola y ventana, los datos en pantalla, los botones Menú y Reiniciar, una carpeta `assets/` y el flujo de ramas.

Qué no copiar: el aspecto, las imágenes ni el código. Es trabajo de otro equipo, las imágenes pueden tener autor o licencia, y en una feria dos proyectos casi iguales se notan. Si les gusta el tema espacial, hagan su propia versión con otra paleta, otros planetas y su propio fondo.

---

## 4. Arquitectura

Todo el código va en archivos sueltos en la raíz, sin carpetas de código. Así los imports son `from reglas import ...` y el juego se corre con `python main.py`. Las únicas carpetas son de apoyo.

```
torre-de-hanoi/
├── README.md
├── .gitignore
├── torres.py          # pilas: push, pop, tope, crear_torres
├── reglas.py          # estado del juego, validar, mover, victoria, mínimo teórico
├── solucion.py        # solución automática con recursión
├── vista.py           # dibujo de las torres en consola y mensajes
├── main.py            # menú y bucle del juego en consola
├── vista_grafica.py   # ventana (segunda vista, opcional)
├── temas.py           # diccionarios de colores y textos de cada tema
├── main_grafico.py    # arranque de la ventana
├── pruebas.py         # casos válidos e inválidos
├── assets/            # imágenes propias, solo si el tema las usa
├── docs/              # documento técnico
└── evidencias/        # capturas de pantalla de las pruebas y del juego
```

Contenido mínimo del `.gitignore` (evita subir archivos temporales y carpetas del editor):

```
__pycache__/
*.pyc
.idea/
.vscode/
```

Dependencias: `main` usa `reglas` y `vista`. `main_grafico` usa `reglas`, `solucion`, `vista_grafica` y `temas`. `reglas` usa `torres`. `solucion`, `vista` y `temas` no usan nada de los demás. `pruebas` usa `reglas` y `solucion`. Nadie importa a `main` ni a `main_grafico`.

### Contrato de funciones (se acuerda antes de programar)

Con esta tabla cada persona programa su parte sin esperar a las demás.

| Archivo | Función | Recibe | Devuelve |
|---------|---------|--------|----------|
| `torres.py` | `push(pila, disco)` | pila, disco | nada |
| `torres.py` | `pop(pila)` | pila | el disco retirado |
| `torres.py` | `tope(pila)` | pila | disco de arriba o `None` |
| `torres.py` | `crear_torres(n)` | cantidad de discos | `[[n, ..., 1], [], []]` |
| `reglas.py` | `crear_juego(n)` | cantidad de discos | diccionario con `discos`, `torres`, `movimientos` |
| `reglas.py` | `minimo_teorico(n)` | cantidad de discos | `2 ** n - 1` |
| `reglas.py` | `validar_movimiento(juego, origen, destino)` | índices 0 a 2 | `(True, "")` o `(False, motivo)` |
| `reglas.py` | `mover_disco(juego, origen, destino)` | índices 0 a 2 | `(valido, motivo)`; si es válido, mueve y suma 1 al contador |
| `reglas.py` | `hay_victoria(juego)` | juego | `True` si todos los discos están en la torre destino |
| `solucion.py` | `resolver(n, origen, destino, auxiliar, pasos)` | discos, torres 0 a 2, lista vacía | nada; llena `pasos` con tuplas `(origen, destino)` en orden |
| `vista.py` | `mostrar_juego(juego)` | juego | nada (imprime torres, movimientos y mínimo) |
| `main.py` | `pedir_discos()`, `pedir_torre(texto)`, `jugar()` | | |

`resolver` resuelve desde el estado inicial. Para el botón Resolver de la ventana, primero se reinicia la partida y después se recorren los pasos con `after`.

Convención: dentro del código las torres son 0, 1 y 2. Al jugador se le muestran como 1, 2 y 3 (origen, auxiliar y destino).

---

## 5. La pila como estructura de datos

Cada torre es una lista. El último elemento es el tope. El valor guardado es el tamaño del disco (1 es el más pequeño).

```
torre origen con 3 discos:  [3, 2, 1]
                             ^        ^
                           base      tope
```

Por qué una pila encaja: en Hanói solo se puede tocar el disco de arriba, que es la definición de LIFO. `push` apila, `pop` retira, `tope` mira sin retirar. La regla "no poner uno grande sobre uno pequeño" se reduce a comparar el disco que se mueve con `tope(destino)`.

Frase para la defensa: *"Cada torre es una pila porque solo el último disco que entró puede salir."*

---

## 6. Reglas y mensajes de rechazo

El juego tiene que rechazar el movimiento y explicar el motivo. Esta es la lista completa, en el orden en que se revisa:

| Orden | Condición | Mensaje |
|-------|-----------|---------|
| 1 | Origen o destino fuera de 1 a 3 (o texto no numérico) | "Esa torre no existe. Usa 1, 2 o 3." |
| 2 | Origen igual a destino | "El origen y el destino son la misma torre." |
| 3 | La torre origen está vacía | "La torre de origen está vacía, no hay disco que mover." |
| 4 | Disco a mover mayor que el tope del destino | "No puedes poner el disco 3 sobre el disco 1, que es más pequeño." |

"Solo el disco de arriba" no necesita una regla aparte: `pop` siempre saca el tope, así que es imposible mover otro. Se demuestra con una prueba.

---

## 7. Código borrador

Borrador de referencia con el estilo del repo (funciones, comentarios en español, nombres en español). No se ejecuta el desarrollo hasta que el equipo apruebe el plan.

### `torres.py`

```python
# torres.py: las torres son pilas (listas donde el tope es el ultimo elemento)

def push(pila, disco):
    pila.append(disco)

def pop(pila):
    return pila.pop()

def tope(pila):
    # devuelve el disco de arriba sin retirarlo, o None si la pila esta vacia
    if len(pila) == 0:
        return None
    return pila[-1]

def crear_torres(cantidad_discos):
    # el disco mas grande entra primero, asi queda abajo
    torres = [[], [], []]
    for disco in range(cantidad_discos, 0, -1):
        push(torres[0], disco)
    return torres
```

### `reglas.py`

```python
# reglas.py: estado del juego y reglas de Hanoi
from torres import push, pop, tope, crear_torres

def crear_juego(cantidad_discos):
    return {"discos": cantidad_discos,
            "torres": crear_torres(cantidad_discos),
            "movimientos": 0}

def minimo_teorico(cantidad_discos):
    return 2 ** cantidad_discos - 1

def validar_movimiento(juego, origen, destino):
    torres = juego["torres"]
    if origen < 0 or origen > 2 or destino < 0 or destino > 2:
        return (False, "Esa torre no existe. Usa 1, 2 o 3.")
    if origen == destino:
        return (False, "El origen y el destino son la misma torre.")
    disco = tope(torres[origen])
    if disco is None:
        return (False, "La torre de origen esta vacia, no hay disco que mover.")
    encima = tope(torres[destino])
    if encima is not None and disco > encima:
        return (False, f"No puedes poner el disco {disco} sobre el disco {encima}, que es mas pequeño.")
    return (True, "")

def mover_disco(juego, origen, destino):
    valido, motivo = validar_movimiento(juego, origen, destino)
    if valido:
        push(juego["torres"][destino], pop(juego["torres"][origen]))
        juego["movimientos"] += 1
    return (valido, motivo)

def hay_victoria(juego):
    return len(juego["torres"][2]) == juego["discos"]
```

### `vista.py`

```python
# vista.py: dibujo de las torres en consola
from reglas import minimo_teorico

def mostrar_juego(juego):
    n = juego["discos"]
    ancho = n * 2 + 8   # deja espacio para las etiquetas de abajo
    print()
    for nivel in range(n - 1, -1, -1):
        fila = ""
        for torre in juego["torres"]:
            if nivel < len(torre):
                fila += ("#" * (torre[nivel] * 2 - 1)).center(ancho)
            else:
                fila += "|".center(ancho)
        print(fila)
    print("1 ORIGEN".center(ancho) + "2 AUXILIAR".center(ancho) + "3 DESTINO".center(ancho))
    print("Movimientos:", juego["movimientos"], "| Minimo teorico:", minimo_teorico(n))
```

### `main.py`

```python
# main.py: menu y bucle principal
from reglas import crear_juego, mover_disco, hay_victoria, minimo_teorico
from vista import mostrar_juego

def pedir_discos():
    while True:
        texto = input("Cantidad de discos (3 a 8): ")
        if texto.isdigit() and int(texto) >= 3 and int(texto) <= 8:
            return int(texto)
        print("Valor no valido. Escribe un numero entre 3 y 8.")

def pedir_torre(mensaje):
    texto = input(mensaje)
    if texto.isdigit():
        return int(texto) - 1
    return -1   # fuerza el rechazo "esa torre no existe"

def jugar():
    juego = crear_juego(pedir_discos())
    while not hay_victoria(juego):
        mostrar_juego(juego)
        origen = pedir_torre("Mover desde la torre (1-3): ")
        destino = pedir_torre("Mover hacia la torre (1-3): ")
        valido, motivo = mover_disco(juego, origen, destino)
        if not valido:
            print("Movimiento invalido:", motivo)
    mostrar_juego(juego)
    print("Ganaste en", juego["movimientos"], "movimientos.")
    print("El minimo posible era", minimo_teorico(juego["discos"]))

jugar()
```

### `solucion.py`

```python
# solucion.py: solucion automatica con recursion (clases 27 y 28)

def resolver(n, origen, destino, auxiliar, pasos):
    # caso base: sin discos no hay nada que mover
    if n == 0:
        return
    # 1. mover los n-1 discos de arriba a la torre auxiliar
    resolver(n - 1, origen, auxiliar, destino, pasos)
    # 2. mover el disco mas grande al destino
    pasos.append((origen, destino))
    # 3. mover los n-1 discos de la auxiliar al destino
    resolver(n - 1, auxiliar, destino, origen, pasos)
```

Cómo se explica: para mover n discos, primero se mueven n-1 al auxiliar, después el más grande al destino y al final los n-1 sobre él. Cada llamada queda esperando en la pila de llamadas (clase 28) hasta que termina la llamada de adentro. La cantidad de pasos cumple `T(n) = 2 * T(n - 1) + 1` con `T(0) = 0`, que da `2^n - 1`.

### `pruebas.py`

```python
# pruebas.py: casos validos e invalidos. Se ejecuta con: python pruebas.py
from reglas import crear_juego, mover_disco, hay_victoria, minimo_teorico
from solucion import resolver

total = 0
fallos = 0

def comprobar(nombre, obtenido, esperado):
    global total, fallos
    total += 1
    if obtenido == esperado:
        print("OK    ", nombre)
    else:
        fallos += 1
        print("FALLO ", nombre, "| esperado:", esperado, "| obtenido:", obtenido)

# 1. movimiento valido
j = crear_juego(3)
comprobar("mover disco pequeño a torre vacia", mover_disco(j, 0, 1), (True, ""))
comprobar("estado despues del movimiento", j["torres"], [[3, 2], [1], []])

# 2. solo se mueve el disco de arriba
comprobar("el disco 3 sigue en la base", j["torres"][0][0], 3)

# 3. disco grande sobre pequeño
valido, motivo = mover_disco(j, 0, 1)
comprobar("disco 2 sobre disco 1 se rechaza", valido, False)
comprobar("el estado no cambia al rechazar", j["torres"], [[3, 2], [1], []])

# 4. torre origen vacia
j = crear_juego(3)
comprobar("mover desde torre vacia", mover_disco(j, 1, 2)[0], False)

# 5. mismo origen y destino
comprobar("origen igual a destino", mover_disco(j, 0, 0)[0], False)

# 6. torre inexistente
comprobar("torre 5 no existe", mover_disco(j, 0, 5)[0], False)

# 7. contador
j = crear_juego(3)
mover_disco(j, 0, 2)      # valido
mover_disco(j, 0, 2)      # invalido (disco 2 sobre disco 1)
comprobar("el contador solo suma movimientos validos", j["movimientos"], 1)

# 8. minimo teorico
comprobar("minimo con 3 discos", minimo_teorico(3), 7)
comprobar("minimo con 5 discos", minimo_teorico(5), 31)

# 9. victoria
j = crear_juego(3)
comprobar("no hay victoria al inicio", hay_victoria(j), False)
for origen, destino in [(0, 2), (0, 1), (2, 1), (0, 2), (1, 0), (1, 2), (0, 2)]:
    mover_disco(j, origen, destino)
comprobar("victoria al terminar", hay_victoria(j), True)
comprobar("se resolvio en el minimo", j["movimientos"], minimo_teorico(3))

# 10. solucion automatica (recursion): gana y usa el minimo de movimientos
for n in [3, 4, 5, 8]:
    j = crear_juego(n)
    pasos = []
    resolver(n, 0, 2, 1, pasos)
    for origen, destino in pasos:
        mover_disco(j, origen, destino)
    comprobar("resolver gana con " + str(n) + " discos", hay_victoria(j), True)
    comprobar("resolver usa el minimo con " + str(n) + " discos", j["movimientos"], minimo_teorico(n))

print("\nTotal:", total, "| Fallos:", fallos)
```

---

## 8. Pruebas y evidencias

| # | Caso | Tipo | Resultado esperado |
|---|------|------|--------------------|
| 1 | Mover el disco de arriba a una torre vacía | Válido | Se mueve |
| 2 | Tras mover, el disco grande sigue en su base | Válido | Solo se movió el disco superior |
| 3 | Disco grande sobre disco pequeño | Inválido | Rechazo con motivo, estado intacto |
| 4 | Mover desde una torre vacía | Inválido | Rechazo con motivo |
| 5 | Mismo origen y destino | Inválido | Rechazo con motivo |
| 6 | Torre inexistente (0, 4, letras) | Inválido | Rechazo con motivo |
| 7 | Contador con un movimiento válido y uno inválido | Conteo | Suma solo el válido |
| 8 | Mínimo teórico para 3 y 5 discos | Cálculo | 7 y 31 |
| 9 | Secuencia óptima de 7 movimientos con 3 discos | Victoria | Detecta victoria en 7 movimientos |
| 10 | Cantidad de discos: letras, 0, 2, 9 | Inválido | `pedir_discos` vuelve a preguntar (prueba manual con captura, porque depende de `input`) |
| 11 | Solución automática con 3, 4, 5 y 8 discos | Recursión | Termina en victoria usando el mínimo de movimientos |

Evidencias para la entrega (carpeta `evidencias/`):

1. Captura de `python pruebas.py` con todo en OK.
2. Captura de una partida con un movimiento válido.
3. Captura de cada rechazo (casos 3, 4, 5 y 6), mostrando el mensaje.
4. Captura de la pantalla de victoria con el mínimo teórico.
5. Si se hace la ventana: una captura de cada tema y de un rechazo mostrado en pantalla.

Canvas pide evidencias de movimientos válidos e inválidos, así que cada captura de un rechazo debe mostrar bien el mensaje (casos 3 a 6 y 10).

---

## 9. Reparto para 4 personas

Cada integrante es dueño de sus archivos y los explica en la defensa.

| # | Responsable de | Entrega | En la defensa explica |
|---|----------------|---------|-----------------------|
| 1 | Estructura, reglas y recursión | `torres.py`, `reglas.py`, `solucion.py` | La pila (`push`, `pop`, `tope`), las 4 validaciones, el diccionario de estado, la victoria y la recursión de `resolver` |
| 2 | Consola | `vista.py`, `main.py` | Cómo se dibuja cada nivel, la validación de entradas, el bucle y los mensajes |
| 3 | Ventana y temas | `vista_grafica.py`, `temas.py`, `main_grafico.py` | Cómo un clic llega a `mover_disco`, cómo cambia el tema y cómo funciona el botón Resolver |
| 4 | Pruebas y documentación | `pruebas.py`, `evidencias/`, `docs/`, `README.md`, guion de la demo | Cada caso de prueba y qué regla comprueba |

Cómo se equilibra la carga:

- La persona 1 tiene poco código pero es de la que todo depende. Termina primero, ayuda a integrar y después apoya en la ventana (por ejemplo, el botón Resolver).
- La persona 2 termina la consola pronto y pasa a ayudar con la ventana (selector de discos y botones).
- La persona 4 empieza `pruebas.py` el primer día, contra el contrato de funciones, sin esperar a que el código exista.

Canvas habla de 5 integrantes. Un equipo de 4 funciona con este reparto, pero conviene confirmarlo con el docente para que no afecte la nota.

Revisión cruzada: 1 revisa el archivo de 2, 2 el de 3, 3 el de 4 y 4 el de 1. Así cada quien conoce al menos dos partes, lo que ayuda en la defensa individual.

---

## 10. Calendario

Hoy es viernes 13 de noviembre. La entrega es en la primera semana de diciembre, día sin confirmar. El 1 de diciembre cae martes, así que el cierre interno es el sábado 28 de noviembre y lo que quede después es colchón, no tiempo de trabajo.

| Cuándo | Objetivo | Quién |
|--------|----------|-------|
| Vie 13 y sáb 14 nov | Contrato de funciones y reparto aprobados, repo creado, preguntas enviadas al docente, versión de Python y `tkinter` comprobados, librería de la ventana propuesta | Todos |
| Lun 16 a sáb 21 nov | `torres.py`, `reglas.py` y `solucion.py` con `pruebas.py` en OK. Consola integrada y jugable. La persona 3 practica y dibuja torres y discos fijos | 1 y 4 con el núcleo y las pruebas, 2 con la consola, 3 con la ventana |
| Lun 23 a sáb 28 nov | Ventana conectada a las reglas, temas, botones Reiniciar y Resolver, evidencias finales, documento técnico y README | 3 con apoyo de 2 y 1, 4 con el documento |
| Lun 30 nov hasta la entrega | Colchón: ensayo de defensa y de feria, ajustes que pida el docente y temas de clases nuevas | Todos |

Si ya avanzaron algo, márquenlo en el checklist de la sección 15. El calendario no se mueve: lo que se adelanta se convierte en colchón.

Puntos de control:

- Sáb 14 nov: contrato aprobado y repo creado.
- Sáb 21 nov: consola jugable y `pruebas.py` en OK. Si no lo está, la ventana se congela hasta que lo esté. Ese día también se confirma la librería de la ventana.
- Sáb 28 nov: todo lo obligatorio listo para entregar. La ventana entra si funciona. Si no, se presenta la consola.

Dependencia principal: la integración no empieza hasta que cada archivo corra solo.

### Extras, en este orden y solo si lo obligatorio está cerrado

1. Botón Resolver (solución automática con `resolver` y `after`). Ahora que la recursión está vista, es el extra con mejor relación entre esfuerzo e impacto, sobre todo en feria.
2. Opción en consola para mostrar los pasos de la solución.
3. Deshacer el último movimiento con otra pila.
4. Más temas.

---

## 11. Cobertura de requisitos de la guía

| Requisito de Canvas | Dónde se cumple | Prueba |
|---------------------|-----------------|--------|
| Tres torres: origen, auxiliar y destino | `crear_torres` y `vista.py` | 1 |
| Un disco a la vez, solo el de arriba | `mover_disco` con `pop` | 1, 2 |
| No poner un disco grande sobre uno pequeño | `validar_movimiento` | 3 |
| Detectar el objetivo automáticamente | `hay_victoria` | 9 |
| Rechazar movimientos inválidos y explicar el motivo | `validar_movimiento` devuelve el motivo | 3, 4, 5, 6 |
| Configurar la cantidad de discos | `pedir_discos` | 10 |
| Mostrar el estado de las torres | `mostrar_juego` | captura |
| Contar y mostrar movimientos | `juego["movimientos"]` | 7 |
| Mostrar el mínimo `2^n - 1` | `minimo_teorico` | 8 |
| Pilas como estructura | `torres.py` | 1, 2 |
| Código modular y comentado | Cinco archivos con comentarios | revisión cruzada |
| Pruebas válidas e inválidas | `pruebas.py` | todas |

Entregables de Canvas: código fuente (sección 4), documento técnico (semana 3), evidencias (sección 8), demostración y participación individual (sección 9).

---

## 12. Riesgos

| Riesgo | Qué hacer |
|--------|-----------|
| Un archivo no corre porque falta un `import` | Los imports se prueban en la semana 1, antes de integrar |
| Cada quien programa con nombres distintos | El contrato de la sección 4 es la ley. Cualquier cambio se avisa al grupo. |
| El usuario escribe letras en lugar de números | `.isdigit()` antes de convertir. Es el caso de prueba 6 y 10. |
| Alguien no entiende su parte para la defensa | Revisión cruzada y ensayo con preguntas entre el equipo |
| Cambios que pisan el trabajo de otro | Un archivo por persona. Si dos tocan el mismo, se avisa antes. |
| Entrega más cerca de lo esperado | Prioridad: reglas y pilas, luego pruebas, luego consola, luego ventana. Los extras van al final. |
| `tkinter` no abre en la máquina de alguien | Probarlo en la semana 1 y usar el Python de Windows si alguien trabaja en WSL |
| La ventana se come el tiempo de lo obligatorio | Punto de control del 21 de noviembre: si la consola no está integrada, la ventana se congela |
| Elegir la librería gráfica tarde o cambiarla a la mitad | Se decide antes del 21 de noviembre. Las reglas no cambian, pero rehacer la ventana cuesta días |
| Copiar el aspecto del proyecto de otro equipo | Inspirarse sí, copiar no: paleta, fondo y textos propios. En una feria se nota |
| Imágenes de terceros sin licencia | Dibujar las propias o usar paquetes con licencia libre (por ejemplo CC0) y anotar la fuente |

---

## 13. Preguntas pendientes

### Para el docente

Sobre el proyecto. Si el docente no responde alguna, se sigue con lo de la tercera columna. La cuarta es para anotar su respuesta.

| # | Pregunta | Si no responde, asumimos | Respuesta |
|---|----------|--------------------------|-----------|
| 1 | ¿La pila puede ser una lista de Python con funciones `push` y `pop` (clase 16), o esperan una clase `Pila` o una pila hecha con `Nodo`? | Lista con `push` y `pop` | |
| 2 | ¿La consola alcanza la nota completa, o la interfaz gráfica suma? ¿Se permite `tkinter` u otra librería? | Consola completa y ventana como segunda vista | |
| 3 | ¿La torre destino es siempre la tercera? | Origen es la 1 y destino la 3 | |
| 4 | ¿Un movimiento inválido cuenta en el contador? | No, solo los válidos | |
| 5 | ¿Las pruebas pueden ser un script propio que muestre OK o FALLO, con capturas? | Sí, `pruebas.py` más capturas | |
| 6 | ¿Suman los extras, como la solución automática con recursión o deshacer? | Son opcionales y van al final | |
| 7 | ¿Podemos usar `from archivo import funcion` para dividir el código? | Sí | |
| 8 | ¿Hay un mínimo y un máximo de discos? | De 3 a 8 | |
| 9 | Al ganar, ¿el juego termina o debe ofrecer jugar de nuevo? | Vuelve al menú | |
| 10 | ¿El mensaje de rechazo debe decir qué regla se rompió? | Sí, uno por regla | |
| 11 | Para entradas inválidas, ¿esperan `try/except` o basta con `isdigit()`? | Basta con `isdigit()` | |
| 12 | ¿Qué esperan en el documento técnico? | Pila, funciones, validaciones, recursión y la fórmula | |

Sobre la entrega, la feria y la defensa:

| # | Pregunta | Respuesta |
|---|----------|-----------|
| 13 | ¿Cuál es la fecha exacta de entrega? Canvas muestra `[DD/MM/AAAA]` | |
| 14 | ¿Es feria de logros, solo defensa, o las dos? Si hay feria, ¿cuándo, dónde y cuánto dura la demo? | |
| 15 | ¿Llevamos nuestra computadora o proveen una? Si la proveen, ¿qué versión de Python tiene y trae `tkinter`? | |
| 16 | ¿La feria se califica aparte de la defensa? ¿Quién evalúa? | |
| 17 | En la defensa, ¿evalúan también el código de la ventana aunque no se vio en clase? | |
| 18 | ¿Un equipo de 4 está bien, siendo que Canvas dice 5? | |
| 19 | ¿Cómo se evalúa la participación individual? | |
| 20 | ¿Se entrega por Canvas o por GitHub? ¿Puede ser público? ¿Piden material extra para la feria, como póster? | |

Si solo pueden hacer pocas preguntas, que sean la 1, 2, 13, 14 y 18. Son las que más cambian lo que van a programar y cómo se reparten el tiempo.

Mensaje corto, listo para enviar:

```
Buenas, profesor. Sobre el proyecto de la Torre de Hanói, nos gustaría confirmar algunos puntos antes de avanzar:

1. ¿La pila puede ser una lista de Python con funciones push y pop, o prefiere una clase Pila o Nodo?
2. ¿La versión de consola alcanza la nota completa, o la interfaz gráfica suma puntos? ¿Podemos usar tkinter?
3. ¿Cuál es la fecha exacta de entrega? En Canvas aparece [DD/MM/AAAA].
4. ¿Se presenta en una feria de logros, solo en defensa, o las dos? Si hay feria, ¿cuánto dura la demo?
5. Somos 4 integrantes y Canvas dice 5. ¿Hay algún inconveniente?
6. ¿Las pruebas pueden ser un script propio que muestre OK o FALLO, con capturas?
7. ¿Suman los extras, como una solución automática con recursión?
8. ¿Qué espera que expliquemos en el documento técnico?

Muchas gracias.
```

### Para decidir entre ustedes

1. ¿Quién se encarga de la ventana y con qué librería?
2. ¿Qué versión de Python y qué sistema usa cada quien? ¿Alguien trabaja en WSL?
3. ¿En qué cuenta de GitHub va el repo y quién tiene permisos de escritura?
4. ¿Qué día y a qué hora se reúnen cada semana?
5. ¿Qué tema se elige? Propuesta: Clásico por defecto y uno propio.
6. ¿Clics sobre las torres o botones de origen y destino? Recomiendo clics.
7. ¿Qué rango de discos? Propuesta: 3 a 8.

---

## 14. Revisión del repo ETD

Última revisión: 13 de noviembre de 2026. El repo llega hasta la clase 28.

| Punto | Resultado |
|-------|-----------|
| Seguridad | Sin hallazgos: ni `.env`, ni claves, ni contraseñas |
| Estilo | Comentarios línea por línea en español, funciones simples y menú con `while True` |
| README y `.gitignore` | No existen. Para el repo del equipo conviene crear ambos |
| Contenido visto | Variables, strings, listas, tuplas, conjuntos, diccionarios, condicionales, funciones, pilas, colas, árboles BST, grafos, matriz de adyacencia, recursividad y pila de llamadas |
| Nuevo desde la última revisión | `clase27/Recursividad.py` (factorial), `clase28/CallStack.py` (suma recursiva) y `clase28/iteraciones.py` (la misma suma con `for`) |

Todavía no aparecen imports entre archivos, `try/except`, manejo de archivos, `tkinter` ni `pygame`. Si el docente agrega alguno, se actualiza este plan.

---

## 15. Checklist de entrega

- [ ] Fecha y formato de presentación confirmados con el docente
- [ ] Equipo de 4 confirmado
- [ ] Repo creado con permisos para los cuatro, README y `.gitignore`
- [ ] Contrato de funciones aprobado (14 nov)
- [ ] `torres.py`, `reglas.py` y `solucion.py` con `pruebas.py` en OK
- [ ] Consola jugable de principio a fin (21 nov)
- [ ] Librería de la ventana decidida (21 nov) y comprobada en la computadora de cada integrante
- [ ] Ventana conectada a las reglas, con al menos dos temas y botones Reiniciar y Resolver
- [ ] Capturas en `evidencias/` (consola y ventana)
- [ ] Documento técnico en `docs/`, revisado por el dueño de cada archivo (28 nov)
- [ ] Ensayo de defensa y de feria hecho, cada integrante explica su parte

---

## 16. Esquema del documento técnico y de la defensa

### Documento técnico (2 a 4 páginas, formato por confirmar)

| Parte | Contenido |
|-------|-----------|
| 1. Datos del equipo | Nombres, curso, docente y fecha |
| 2. Descripción | Qué es el juego y sus tres reglas |
| 3. Estructura de datos | La pila (LIFO), cómo se representa cada torre, `push`, `pop`, `tope` y por qué encaja |
| 4. Estado del juego | El diccionario (`discos`, `torres`, `movimientos`) y el recorrido de un movimiento, de la entrada a la actualización |
| 5. Funciones | Una tabla por archivo con nombre, qué recibe y qué devuelve (la del contrato de la sección 4) |
| 6. Validaciones | Las 4 reglas de rechazo con su mensaje (sección 6) |
| 7. Recursión | `resolver`, el caso base, la pila de llamadas (clase 28) y por qué da `2^n - 1` pasos |
| 8. Pruebas | Tabla de casos y capturas |
| 9. Interfaz | Consola y ventana, con una captura de cada tema |
| 10. Conclusiones | Qué aprendieron y qué mejorarían |

### Guion de defensa y de feria

| Tiempo | Qué pasa | Quién |
|--------|----------|-------|
| 1 minuto | Qué es el juego y por qué las torres son pilas | 1 |
| 2 minutos | Demo: un movimiento válido, uno inválido con su mensaje, la victoria con el mínimo y el botón Resolver | 3, con 2 apoyando |
| 1 minuto por persona | Cada uno explica su archivo | Todos |
| 1 minuto | Pruebas: correr `pruebas.py` y mostrar el OK | 4 |

Preguntas que conviene tener ensayadas:

| Pregunta | Respuesta corta |
|----------|-----------------|
| ¿Por qué una pila? | Solo se puede sacar el último disco que entró (LIFO), y `pop` siempre saca el tope |
| ¿Cómo se sabe que un movimiento es inválido? | `validar_movimiento` revisa en orden: torre inexistente, mismo origen y destino, origen vacío y disco grande sobre pequeño |
| ¿Por qué el contador no sube con un movimiento inválido? | `mover_disco` solo suma si `validar_movimiento` devuelve `True` |
| ¿De dónde sale `2^n - 1`? | Mover n discos cuesta dos veces mover n-1, más uno: `T(n) = 2 * T(n - 1) + 1` |
| ¿Qué pasa cuando `n` llega a 0 en `resolver`? | Es el caso base: no hay nada que mover y la función termina sin más llamadas |
| ¿Qué relación hay entre la recursión y una pila? | Cada llamada queda esperando en la pila de llamadas hasta que termina la de adentro (clase 28) |
| ¿Cómo se sabe que ganó? | `hay_victoria` compara cuántos discos hay en la torre destino contra el total |
| (Ventana) ¿Cómo llega un clic a la regla? | `clic -> al_hacer_clic -> intentar_mover -> mover_disco -> validar_movimiento -> push y pop -> dibujar` |

---

## 17. Trabajo en equipo con Git

| Regla | Detalle |
|-------|---------|
| Una rama por tarea | `feature/torres`, `feature/consola`, `feature/ventana`, `feature/pruebas` |
| Un archivo, un dueño | Si alguien necesita tocar el archivo de otro, avisa antes |
| `git pull` antes de empezar | Evita conflictos |
| Commits cortos y claros | Qué se hizo, en una línea |
| `main` siempre corre | Una rama se une a `main` solo si `python pruebas.py` da todo en OK |

Comandos para cada tarea (copiar y pegar):

```bash
git checkout main
git pull
git checkout -b feature/consola

# ... trabajar ...

git add .
git commit -m "consola: dibuja las torres y valida entradas"
git push -u origin feature/consola
```

Después se abre un Pull Request en GitHub y otra persona lo revisa (la revisión cruzada de la sección 9) antes de unirlo a `main`.