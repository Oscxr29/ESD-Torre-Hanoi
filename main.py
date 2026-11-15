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
    while True:
        juego = crear_juego(pedir_discos())
        while not hay_victoria(juego):
            mostrar_juego(juego)
            origen = pedir_torre("Mover desde la torre (1-3): ")
            destino = pedir_torre("Mover hacia la torre (1-3): ")
            valido, motivo = mover_disco(juego, origen, destino)
            if not valido:
                print("Movimiento invalido:", motivo)
        mostrar_juego(juego)
        print("¡Ganaste en", juego["movimientos"], "movimientos!")
        print("El minimo posible era", minimo_teorico(juego["discos"]))
        
        repetir = input("\n¿Deseas jugar otra partida? (s/n): ").strip().lower()
        if repetir != "s":
            print("¡Gracias por jugar! Hasta pronto.")
            break

jugar()
