"""
model.py - Capa de Modelo (MVC)
Gestiona la entidad Producto y las operaciones con la base de datos SQLite.
"""

import sqlite3
from dataclasses import dataclass
from typing import Optional


# ──────────────────────────────────────────────
# Entidad
# ──────────────────────────────────────────────

@dataclass
class Producto:
    nombre: str
    cantidad: int
    precio: float
    id: Optional[int] = None

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - Cant: {self.cantidad} - Precio: ${self.precio:.2f}"


# ──────────────────────────────────────────────
# Repositorio (acceso a datos)
# ──────────────────────────────────────────────

class ProductoRepository:
    """Gestiona todas las operaciones CRUD sobre la tabla 'productos'."""

    def __init__(self, db_path: str = "inventario.db"):
        self._db_path = db_path
        self._conn = sqlite3.connect(self._db_path)
        self._conn.row_factory = sqlite3.Row   # acceso por nombre de columna
        self._crear_tabla()

    # ---------- conexión ----------

    def _conectar(self) -> sqlite3.Connection:
        return self._conn

    def _crear_tabla(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS productos (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre   TEXT    NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            precio   REAL    NOT NULL DEFAULT 0.0
        );
        """
        self._conn.execute(sql)
        self._conn.commit()

    # ---------- CRUD ----------

    def agregar(self, producto: Producto) -> int:
        """Inserta un nuevo producto y devuelve su id generado."""
        sql = "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)"
        cursor = self._conn.execute(sql, (producto.nombre, producto.cantidad, producto.precio))
        self._conn.commit()
        return cursor.lastrowid

    def obtener_todos(self) -> list[Producto]:
        """Devuelve todos los productos ordenados por nombre."""
        sql = "SELECT * FROM productos ORDER BY nombre"
        filas = self._conn.execute(sql).fetchall()
        return [Producto(fila["nombre"], fila["cantidad"], fila["precio"], fila["id"])
                for fila in filas]

    def obtener_por_id(self, producto_id: int) -> Optional[Producto]:
        """Devuelve un producto por su id, o None si no existe."""
        sql = "SELECT * FROM productos WHERE id = ?"
        fila = self._conn.execute(sql, (producto_id,)).fetchone()
        if fila is None:
            return None
        return Producto(fila["nombre"], fila["cantidad"], fila["precio"], fila["id"])

    def actualizar(self, producto: Producto) -> bool:
        """Actualiza un producto existente. Devuelve True si se modificó."""
        sql = "UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?"
        cursor = self._conn.execute(sql, (producto.nombre, producto.cantidad,
                                          producto.precio, producto.id))
        self._conn.commit()
        return cursor.rowcount > 0

    def eliminar(self, producto_id: int) -> bool:
        """Elimina un producto por su id. Devuelve True si se eliminó."""
        sql = "DELETE FROM productos WHERE id = ?"
        cursor = self._conn.execute(sql, (producto_id,))
        self._conn.commit()
        return cursor.rowcount > 0

    def buscar(self, texto: str) -> list[Producto]:
        """Busca productos cuyo nombre contenga el texto (case-insensitive)."""
        sql = "SELECT * FROM productos WHERE nombre LIKE ? ORDER BY nombre"
        filas = self._conn.execute(sql, (f"%{texto}%",)).fetchall()
        return [Producto(fila["nombre"], fila["cantidad"], fila["precio"], fila["id"])
                for fila in filas]
