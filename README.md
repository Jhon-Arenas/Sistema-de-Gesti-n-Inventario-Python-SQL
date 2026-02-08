# 📦 Sistema de Gestión de Inventario - Inventos Pro

> Versión 0.2: Modularización y Portabilidad

## 📝 Descripción
Software de escritorio para el control de inventarios, desarrollado con un enfoque en la experiencia de usuario moderna y la facilidad de despliegue.

## 🚀 ¿Qué hay de nuevo en esta versión?
- **Modularización:** El código se ha separado en archivos independientes por sección, siguiendo principios de limpieza y mantenimiento.
- **Portabilidad con SQLite:** Cambio de SQL Server a SQLite, eliminando la necesidad de servidores externos.
- **Rutas Dinámicas:** Implementación de lógica para que el programa detecte su ubicación y encuentre sus recursos automáticamente.
- **Exportación de Datos:** Nuevo botón para generar reportes en Excel (.xlsx) de manera instantánea.

## 🛠️ Tecnologías y Librerías
- **Python 3.x**
- **CustomTkinter** (Interfaz de usuario)
- **SQLite3** (Base de datos local)
- **Pandas** (Procesamiento de datos)
- **Openpyxl** (Motor de Excel)

## 📁 Estructura del Repositorio
- `Ventana_principal.py`: Archivo principal.
- `Seccion_reportes.py`: Módulo de estadísticas y exportación.
- `conexion_base.py`: Lógica de conexión portable.
- `inventario.db`: Archivo de base de datos.
