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