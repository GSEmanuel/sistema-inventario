"""
main.py - Punto de entrada de la aplicación
Instancia el Modelo, la Vista y el Controlador (patrón MVC).
"""

from model import ProductoRepository
from view import InventarioView
from controller import InventarioController


def main():
    repo  = ProductoRepository("inventario.db")   # Modelo
    view  = InventarioView()                       # Vista
    InventarioController(view, repo)               # Controlador (wires todo)
    view.mainloop()


if __name__ == "__main__":
    main()
