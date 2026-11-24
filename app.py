# app.py: servidor web con Flask para la Torre de Hanói
import webbrowser
from flask import Flask, render_template, request, jsonify

# Importamos exactamente la lógica ya construida (sin modificarla)
from reglas import crear_juego, mover_disco, hay_victoria, minimo_teorico
from solucion import resolver
from temas import TEMAS

app = Flask(__name__)

# Estado en memoria de la partida actual
estado = {
    "juego": crear_juego(3),
    "tema": "navidad_noche"
}

@app.route("/")
def index():
    """Sirve la página web principal del juego."""
    return render_template("index.html")

@app.route("/api/estado", methods=["GET"])
def obtener_estado():
    """Devuelve el estado actual de la partida, torres y métricas."""
    j = estado["juego"]
    return jsonify({
        "discos": j["discos"],
        "torres": j["torres"],
        "movimientos": j["movimientos"],
        "minimo": minimo_teorico(j["discos"]),
        "victoria": hay_victoria(j),
        "tema": estado["tema"]
    })

@app.route("/api/iniciar", methods=["POST"])
def iniciar():
    """Reinicia la partida con la cantidad de discos seleccionada (3 a 8)."""
    discos = int(request.json.get("discos", 3))
    estado["juego"] = crear_juego(discos)
    j = estado["juego"]
    return jsonify({
        "discos": j["discos"],
        "torres": j["torres"],
        "movimientos": j["movimientos"],
        "minimo": minimo_teorico(j["discos"]),
        "victoria": False
    })

@app.route("/api/mover", methods=["POST"])
def mover():
    """Valida y ejecuta un movimiento de disco entre torres usando reglas.py."""
    datos = request.json or {}
    origen = int(datos.get("origen", -1))
    destino = int(datos.get("destino", -1))

    # Soporte serverless y multijugador: si el cliente envía su partida, la usamos
    if "juego" in datos and isinstance(datos["juego"], dict):
        j = datos["juego"]
    else:
        j = estado["juego"]

    valido, motivo = mover_disco(j, origen, destino)
    return jsonify({
        "valido": valido,
        "motivo": motivo,
        "torres": j["torres"],
        "movimientos": j["movimientos"],
        "minimo": minimo_teorico(j["discos"]),
        "victoria": hay_victoria(j)
    })

@app.route("/api/resolver", methods=["POST"])
def resolver_hanoi():
    """Calcula y devuelve los pasos óptimos usando recursión (solucion.py)."""
    discos = request.json.get("discos") if (request.is_json and request.json) else None
    if discos is None:
        discos = estado["juego"]["discos"]
    else:
        discos = int(discos)
    pasos = []
    resolver(discos, 0, 2, 1, pasos)
    return jsonify({"pasos": pasos, "total": len(pasos)})

@app.route("/api/temas", methods=["GET"])
def obtener_temas():
    """Devuelve los temas visuales disponibles."""
    return jsonify(TEMAS)

if __name__ == "__main__":
    puerto = 5000
    print(f"Servidor activo en: http://localhost:{puerto}")
    webbrowser.open(f"http://localhost:{puerto}")
    app.run(port=puerto, debug=False)
