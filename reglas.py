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