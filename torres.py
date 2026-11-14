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