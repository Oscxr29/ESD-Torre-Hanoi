# main_grafico.py: punto de entrada para la version grafica con tkinter
import tkinter as tk
from temas import TEMAS
from vista_grafica import VistaHanoi

def main():
    root = tk.Tk()
    tema = TEMAS["navidad_noche"]
    VistaHanoi(root, tema)
    root.mainloop()

main()
