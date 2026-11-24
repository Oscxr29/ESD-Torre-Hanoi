# main.py: punto de entrada principal del juego (Modo Web en el Navegador)
import webbrowser
from app import app

def main():
    puerto = 5000
    print("=" * 60)
    print("  TORRE DE HANOI - EDICION NAVIDEÑA (MODO WEB)")
    print(f"  Abriendo en tu navegador: http://localhost:{puerto}")
    print("  Presiona Ctrl+C en esta terminal para detener el servidor.")
    print("=" * 60)
    webbrowser.open(f"http://localhost:{puerto}")
    app.run(port=puerto, debug=False)

if __name__ == "__main__":
    main()
