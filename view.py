"""
view.py - Capa de Vista (MVC)
Define toda la interfaz gráfica con Tkinter.
No contiene lógica de negocio; sólo renderiza y expone callbacks.
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class InventarioView(Tk):
    """Ventana principal del sistema de inventario."""

    # ──────────────────────────────────────────
    # Construcción de la UI
    # ──────────────────────────────────────────

    def __init__(self):
        super().__init__()
        self.title("📦 Sistema de Inventario")
        self.geometry("820x540")
        self.resizable(False, False)

        self._construir_widgets()

    def _construir_widgets(self) -> None:
        # ── Título ──────────────────────────────
        ttk.Label(self, text="Sistema de Inventario", font=("Helvetica", 18, "bold")).pack(pady=(14, 4))

        # ── Frame principal ─────────────────────
        frame_main = ttk.Frame(self)
        frame_main.pack(fill="both", expand=True, padx=16, pady=4)

        # ── Panel izquierdo: formulario ─────────
        self._frame_form = ttk.LabelFrame(frame_main, text="Datos del Producto", padding=10)
        self._frame_form.pack(side="left", fill="y", padx=(0, 12))

        # Campo ID (oculto / solo lectura)
        self._id_var = StringVar()

        # Nombre
        ttk.Label(self._frame_form, text="Nombre:").grid(
            row=0, column=0, sticky="w", pady=4)
        self._nombre_var = StringVar()
        self._entry_nombre = ttk.Entry(self._frame_form, textvariable=self._nombre_var, width=22)
        self._entry_nombre.grid(row=0, column=1, padx=6, pady=4)

        # Cantidad
        ttk.Label(self._frame_form, text="Cantidad:").grid(
            row=1, column=0, sticky="w", pady=4)
        self._cantidad_var = StringVar()
        self._entry_cantidad = ttk.Entry(self._frame_form, textvariable=self._cantidad_var, width=22)
        self._entry_cantidad.grid(row=1, column=1, padx=6, pady=4)

        # Precio
        ttk.Label(self._frame_form, text="Precio ($):").grid(
            row=2, column=0, sticky="w", pady=4)
        self._precio_var = StringVar()
        self._entry_precio = ttk.Entry(self._frame_form, textvariable=self._precio_var, width=22)
        self._entry_precio.grid(row=2, column=1, padx=6, pady=4)

        # ── Botones CRUD ────────────────────────
        frame_botones = ttk.Frame(self._frame_form)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=12)

        self._btn_agregar = ttk.Button(frame_botones, text="Agregar", width=12, cursor="hand2")
        self._btn_agregar.grid(row=0, column=0, padx=4, pady=4)

        self._btn_actualizar = ttk.Button(frame_botones, text="Actualizar", width=12,
                                          cursor="hand2", state="disabled")
        self._btn_actualizar.grid(row=0, column=1, padx=4, pady=4)

        self._btn_eliminar = ttk.Button(frame_botones, text="Eliminar", width=12,
                                        cursor="hand2", state="disabled")
        self._btn_eliminar.grid(row=1, column=0, padx=4, pady=4)

        self._btn_limpiar = ttk.Button(frame_botones, text="Limpiar", width=12, cursor="hand2")
        self._btn_limpiar.grid(row=1, column=1, padx=4, pady=4)

        # ── Panel derecho: lista + búsqueda ─────
        frame_derecho = ttk.Frame(frame_main)
        frame_derecho.pack(side="left", fill="both", expand=True)

        # Búsqueda
        frame_busqueda = ttk.Frame(frame_derecho)
        frame_busqueda.pack(fill="x", pady=(0, 6))
        ttk.Label(frame_busqueda, text="Buscar:").pack(side="left")
        self._busqueda_var = StringVar()
        self._entry_busqueda = ttk.Entry(frame_busqueda, textvariable=self._busqueda_var, width=28)
        self._entry_busqueda.pack(side="left", padx=6)
        self._btn_buscar = ttk.Button(frame_busqueda, text="Buscar", cursor="hand2")
        self._btn_buscar.pack(side="left", padx=2)
        self._btn_mostrar_todos = ttk.Button(frame_busqueda, text="Ver todos", cursor="hand2")
        self._btn_mostrar_todos.pack(side="left", padx=2)

        # Tabla (Treeview)
        cols = ("ID", "Nombre", "Cantidad", "Precio")
        self._tree = ttk.Treeview(frame_derecho, columns=cols, show="headings", height=16)
        for col in cols:
            self._tree.heading(col, text=col)
        self._tree.column("ID",       width=40,  anchor="center")
        self._tree.column("Nombre",   width=220, anchor="w")
        self._tree.column("Cantidad", width=80,  anchor="center")
        self._tree.column("Precio",   width=100, anchor="e")

        scrollbar = ttk.Scrollbar(frame_derecho, orient="vertical",
                                  command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        # ── Barra de estado ─────────────────────
        self._estado_var = StringVar(value="Listo.")
        ttk.Label(self, textvariable=self._estado_var, relief="sunken",
                  anchor="w", font=("Helvetica", 9)).pack(
            fill="x", side="bottom", padx=0, pady=0)

    # ──────────────────────────────────────────
    # Propiedades de lectura del formulario
    # ──────────────────────────────────────────

    @property
    def nombre(self) -> str:
        return self._nombre_var.get().strip()

    @property
    def cantidad(self) -> str:
        return self._cantidad_var.get().strip()

    @property
    def precio(self) -> str:
        return self._precio_var.get().strip()

    @property
    def id_seleccionado(self) -> str:
        return self._id_var.get()

    @property
    def texto_busqueda(self) -> str:
        return self._busqueda_var.get().strip()

    # ──────────────────────────────────────────
    # Métodos de actualización de la UI
    # ──────────────────────────────────────────

    def cargar_tabla(self, productos: list) -> None:
        """Recarga el Treeview con la lista de productos."""
        self._limpiar_tabla()
        for p in productos:
            self._tree.insert("", "end",
                              values=(p.id, p.nombre, p.cantidad, f"${p.precio:.2f}"))

    def _limpiar_tabla(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)

    def rellenar_formulario(self, producto_id: str, nombre: str,
                            cantidad: str, precio: str) -> None:
        """Pone los datos de un producto en el formulario para edición."""
        self._id_var.set(producto_id)
        self._nombre_var.set(nombre)
        self._cantidad_var.set(cantidad)
        self._precio_var.set(precio)
        self._btn_actualizar.config(state="normal")
        self._btn_eliminar.config(state="normal")

    def limpiar_formulario(self) -> None:
        """Vacía el formulario y resetea el estado de los botones."""
        self._id_var.set("")
        self._nombre_var.set("")
        self._cantidad_var.set("")
        self._precio_var.set("")
        self._busqueda_var.set("")
        self._btn_actualizar.config(state="disabled")
        self._btn_eliminar.config(state="disabled")
        self._entry_nombre.focus()

    def set_estado(self, mensaje: str) -> None:
        self._estado_var.set(mensaje)

    # ──────────────────────────────────────────
    # Registro de callbacks (desde el Controller)
    # ──────────────────────────────────────────

    def set_on_agregar(self, callback) -> None:
        self._btn_agregar.config(command=callback)

    def set_on_actualizar(self, callback) -> None:
        self._btn_actualizar.config(command=callback)

    def set_on_eliminar(self, callback) -> None:
        self._btn_eliminar.config(command=callback)

    def set_on_limpiar(self, callback) -> None:
        self._btn_limpiar.config(command=callback)

    def set_on_seleccionar(self, callback) -> None:
        self._tree.bind("<<TreeviewSelect>>", callback)

    def set_on_buscar(self, callback) -> None:
        self._btn_buscar.config(command=callback)

    def set_on_mostrar_todos(self, callback) -> None:
        self._btn_mostrar_todos.config(command=callback)

    # ──────────────────────────────────────────
    # Diálogos
    # ──────────────────────────────────────────

    def confirmar(self, mensaje: str) -> bool:
        return messagebox.askyesno("Confirmar", mensaje)

    def mostrar_error(self, mensaje: str) -> None:
        messagebox.showerror("Error", mensaje)

    def mostrar_info(self, mensaje: str) -> None:
        messagebox.showinfo("Información", mensaje)

    def obtener_item_seleccionado(self):
        """Devuelve los valores del ítem seleccionado en el Treeview, o None."""
        seleccion = self._tree.selection()
        if not seleccion:
            return None
        return self._tree.item(seleccion[0])["values"]
