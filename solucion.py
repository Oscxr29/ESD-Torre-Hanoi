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