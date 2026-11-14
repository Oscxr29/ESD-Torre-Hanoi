# main_grafico.py: punto de entrada para la version grafica con tkinter
import tkinter as tk
from temas import TEMAS
from vista_grafica import VistaHanoi

def main():
    root = tk.Tk()
    tema = TEMAS["clasico"]
    VistaHanoi(root, tema)
    root.mainloop()

if __name__ == "__main__":
    main()
