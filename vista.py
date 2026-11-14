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