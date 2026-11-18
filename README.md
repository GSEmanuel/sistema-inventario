# 📦 Sistema de Inventario

Aplicación de escritorio para gestionar el inventario de productos, construida en **Python** con una interfaz gráfica en **Tkinter** y persistencia en **SQLite**. Sigue el patrón de arquitectura **MVC (Modelo-Vista-Controlador)**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/Licencia-MIT-green)

---

## ✨ Características

- **CRUD completo** — Agregar, ver, editar y eliminar productos.
- **Búsqueda en tiempo real** — Filtra productos por nombre (case-insensitive).
- **Interfaz gráfica intuitiva** — Formulario + tabla con scroll, barra de estado y diálogos de confirmación.
- **Base de datos local** — Los datos se persisten automáticamente en un archivo `inventario.db`.
- **Sin dependencias externas** — Usa solo la biblioteca estándar de Python.

---

## 🖼️ Vista Previa

```
┌──────────────────────────────────────────────────────────────┐
│                   Sistema de Inventario                      │
├─────────────────────┬────────────────────────────────────────┤
│ Datos del Producto  │  Buscar: [________] [Buscar] [Ver todos] │
│                     │                                        │
│ Nombre:   [______]  │  ID │ Nombre     │ Cantidad │ Precio   │
│ Cantidad: [______]  │  1  │ Teclado    │ 25       │ $45.99   │
│ Precio:   [______]  │  2  │ Monitor    │ 10       │ $299.00  │
│                     │  3  │ Mouse      │ 50       │ $19.99   │
│ [Agregar][Actualizar]│  ...                                  │
│ [Eliminar] [Limpiar]│                                        │
└─────────────────────┴────────────────────────────────────────┘
│ 📦 3 producto(s) en inventario.                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Arquitectura (MVC)

```
main.py          →  Punto de entrada: instancia las 3 capas
│
├── model.py     →  Modelo: entidad Producto + repositorio SQLite
├── view.py      →  Vista: interfaz gráfica con Tkinter
└── controller.py →  Controlador: lógica de negocio y validación
```

| Capa           | Archivo          | Responsabilidad                                   |
| -------------- | ---------------- | ------------------------------------------------- |
| **Modelo**     | `model.py`       | Define la entidad `Producto` y las operaciones CRUD contra SQLite. |
| **Vista**      | `view.py`        | Renderiza la interfaz gráfica. No contiene lógica de negocio.      |
| **Controlador**| `controller.py`  | Conecta Vista y Modelo, valida entradas y orquesta el flujo.      |
| **Entrada**    | `main.py`        | Instancia las tres capas e inicia el loop principal.               |

---

## 🚀 Instalación y Uso

### Opción 1: Descargar el ejecutable (recomendado)

No necesitás tener Python instalado. Simplemente descargá el ejecutable listo para usar:

1. Andá a la sección de [**Releases**](https://github.com/GSEmanuel/sistema-inventario/releases).
2. Descargá el archivo correspondiente a tu sistema operativo.
3. Ejecutá el archivo descargado. ¡Listo!

| Sistema Operativo | Archivo                          |
| ------------------ | -------------------------------- |
| Windows            | `Sistema_Inventario.exe`         |
| Linux              | `Sistema_Inventario`             |

> [!NOTE]
> La base de datos `inventario.db` se crea automáticamente en la misma carpeta del ejecutable la primera vez que lo abrís.

### Opción 2: Ejecutar desde el código fuente

Si preferís ejecutar desde el código fuente o querés contribuir al proyecto:

#### Requisitos previos

- **Python 3.10+** (Tkinter viene incluido en la instalación estándar de Python).
- No se necesitan dependencias externas ni `pip install`.

> [!TIP]
> En algunas distribuciones de Linux, Tkinter puede no venir preinstalado. Instalalo con:
> ```bash
> # Debian / Ubuntu
> sudo apt install python3-tk
>
> # Fedora
> sudo dnf install python3-tkinter
>
> # Arch
> sudo pacman -S tk
> ```

#### Clonar y ejecutar

```bash
git clone https://github.com/GSEmanuel/sistema-inventario.git
cd sistema-inventario
python main.py
```

La base de datos `inventario.db` se crea automáticamente en el directorio del proyecto la primera vez que se ejecuta.

---

## 📖 Guía de Uso

| Acción        | Cómo hacerlo                                                        |
| ------------- | ------------------------------------------------------------------- |
| **Agregar**   | Completá los campos del formulario y hacé clic en **Agregar**.      |
| **Editar**    | Seleccioná un producto en la tabla, modificá los datos y presioná **Actualizar**. |
| **Eliminar**  | Seleccioná un producto y hacé clic en **Eliminar**. Confirmá en el diálogo. |
| **Buscar**    | Escribí un texto en el campo de búsqueda y presioná **Buscar**.     |
| **Ver todos** | Hacé clic en **Ver todos** para resetear la búsqueda.               |
| **Limpiar**   | Presioná **Limpiar** para vaciar el formulario.                     |

---

## 📁 Estructura del Proyecto

```
sistema-inventario/
├── main.py            # Punto de entrada
├── model.py           # Entidad Producto + repositorio SQLite
├── view.py            # Interfaz gráfica (Tkinter)
├── controller.py      # Lógica de negocio y validación
├── inventario.db      # Base de datos (se genera automáticamente)
├── .gitignore
└── README.md
```

---

## 🗺️ Hoja de Ruta

### ✅ Completado

- [x] Estructura MVC
- [x] CRUD completo de productos (crear, leer, actualizar, eliminar)
- [x] Persistencia en SQLite
- [x] Búsqueda de productos por nombre
- [x] Validación de entradas en el formulario
- [x] Barra de estado con feedback al usuario

### 🔜 Próximamente

- [ ] **Categorías** — Clasificar productos por categoría / tipo.
- [ ] **Exportar a CSV / Excel** — Generar reportes descargables del inventario.
- [ ] **Alertas de stock bajo** — Notificar cuando un producto esté por debajo de un mínimo.
- [ ] **Historial de movimientos** — Registrar entradas y salidas de stock con fecha.
- [ ] **Autenticación de usuarios** — Login básico para controlar el acceso.
- [ ] **Temas visuales** — Modo claro / oscuro y estilos personalizados con `ttkthemes`.
- [ ] **Dashboard** — Panel con métricas: total de productos, valor total del inventario, productos más vendidos.
- [ ] **Gráficos** — Visualización de datos con `matplotlib` (stock por categoría, tendencias).

### 💡 Ideas a futuro

- [ ] Migrar a una arquitectura web (Flask / FastAPI + frontend moderno).
- [ ] Soporte multi-usuario con base de datos remota (PostgreSQL).
- [ ] Lector de código de barras / QR para agilizar el registro.
- [ ] API REST para integración con otros sistemas.

---

## 🛠️ Tecnologías

| Tecnología | Uso                        |
| ---------- | -------------------------- |
| Python     | Lenguaje principal         |
| Tkinter    | Interfaz gráfica (GUI)     |
| SQLite     | Base de datos local        |

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si querés colaborar:

1. Hacé un fork del proyecto.
2. Creá una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Hacé commit de tus cambios (`git commit -m "Agrega nueva funcionalidad"`).
4. Pusheá a tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abrí un Pull Request.

---

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

---

<p align="center">
  Hecho con ❤️ por <a href="https://github.com/GSEmanuel">GSEmanuel</a>
</p>
