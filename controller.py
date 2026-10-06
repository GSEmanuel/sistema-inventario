"""
controller.py - Capa de Controlador (MVC)
Conecta la Vista con el Modelo. Contiene toda la lógica de negocio.
"""

from model import Producto, ProductoRepository
from view import InventarioView


class InventarioController:
    """Orquesta las interacciones entre la Vista y el Repositorio."""

    def __init__(self, view: InventarioView, repo: ProductoRepository):
        self._view = view
        self._repo = repo

        self._registrar_eventos()
        self._cargar_lista()

    # ──────────────────────────────────────────
    # Registro de eventos
    # ──────────────────────────────────────────

    def _registrar_eventos(self) -> None:
        self._view.set_on_agregar(self._agregar)
        self._view.set_on_actualizar(self._actualizar)
        self._view.set_on_eliminar(self._eliminar)
        self._view.set_on_limpiar(self._limpiar)
        self._view.set_on_seleccionar(self._seleccionar)
        self._view.set_on_buscar(self._buscar)
        self._view.set_on_mostrar_todos(self._cargar_lista)

    # ──────────────────────────────────────────
    # Handlers
    # ──────────────────────────────────────────

    def _agregar(self) -> None:
        producto = self._producto_desde_formulario()
        if producto is None:
            return

        nuevo_id = self._repo.agregar(producto)
        self._view.set_estado(f"✅ Producto '{producto.nombre}' agregado (ID: {nuevo_id}).")
        self._limpiar()

    def _actualizar(self) -> None:
        id_str = self._view.id_seleccionado
        if not id_str:
            self._view.mostrar_error("No hay ningún producto seleccionado.")
            return

        producto = self._producto_desde_formulario()
        if producto is None:
            return

        producto.id = int(id_str)
        if self._repo.actualizar(producto):
            self._view.set_estado(f"✏️ Producto '{producto.nombre}' actualizado.")
        else:
            self._view.mostrar_error("No se pudo actualizar el producto.")
        self._limpiar()

    def _eliminar(self) -> None:
        id_str = self._view.id_seleccionado
        if not id_str:
            self._view.mostrar_error("No hay ningún producto seleccionado.")
            return

        valores = self._view.obtener_item_seleccionado()
        nombre = valores[1] if valores else "este producto"

        if not self._view.confirmar(f"¿Eliminar '{nombre}'?"):
            return

        if self._repo.eliminar(int(id_str)):
            self._view.set_estado(f"🗑️ Producto '{nombre}' eliminado.")
        else:
            self._view.mostrar_error("No se pudo eliminar el producto.")
        self._limpiar()

    def _limpiar(self) -> None:
        self._view.limpiar_formulario()
        self._cargar_lista()

    def _seleccionar(self, _event=None) -> None:
        valores = self._view.obtener_item_seleccionado()
        if valores is None:
            return
        producto_id, nombre, cantidad, precio_str = valores
        # precio viene formateado como "$12.50" → quitamos el símbolo
        precio = precio_str.replace("$", "")
        self._view.rellenar_formulario(str(producto_id), nombre, str(cantidad), precio)
        self._view.set_estado(f"📋 Producto '{nombre}' cargado para edición.")

    def _buscar(self) -> None:
        texto = self._view.texto_busqueda
        if not texto:
            self._cargar_lista()
            return
        resultados = self._repo.buscar(texto)
        self._view.cargar_tabla(resultados)
        self._view.set_estado(f"🔍 {len(resultados)} resultado(s) para '{texto}'.")

    def _cargar_lista(self) -> None:
        productos = self._repo.obtener_todos()
        self._view.cargar_tabla(productos)
        self._view.set_estado(f"📦 {len(productos)} producto(s) en inventario.")

    # ──────────────────────────────────────────
    # Utilidades
    # ──────────────────────────────────────────

    def _producto_desde_formulario(self):
        """Valida y construye un Producto con los datos del formulario.
        Devuelve None si la validación falla."""
        nombre   = self._view.nombre
        cantidad = self._view.cantidad
        precio   = self._view.precio

        if not nombre:
            self._view.mostrar_error("El nombre no puede estar vacío.")
            return None

        try:
            cantidad_int = int(cantidad)
            if cantidad_int < 0:
                raise ValueError
        except ValueError:
            self._view.mostrar_error("La cantidad debe ser un número entero positivo.")
            return None

        try:
            precio_float = float(precio)
            if precio_float < 0:
                raise ValueError
        except ValueError:
            self._view.mostrar_error("El precio debe ser un número positivo.")
            return None

        return Producto(nombre=nombre, cantidad=cantidad_int, precio=precio_float)
