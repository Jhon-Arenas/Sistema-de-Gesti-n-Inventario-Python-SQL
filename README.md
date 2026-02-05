# Sistema-de-Gestion-Inventario-Python-SQL
Sistema CRUD para el control de inventario y ventas, con roles de usuario desarrollado en Python y SSQL server

# 📦 Sistema de Control de Inventario y Gestión de Ventas

## 🎯 Objetivo del Proyecto
Optimizar el flujo de información entre el almacén y el punto de venta, garantizando la integridad de los datos y la seguridad por niveles de acceso.

## 🛠️ Especificaciones Técnicas
- **Lenguaje:** Python 3.10+
- **Motor de DB:** SQL Server (T-SQL)
- **Conector:** `pyodbc` utilizando Trusted Connection.
- **Arquitectura:** Modular (Separación de lógica de conexión y ejecución).

## 🔑 Gestión de Roles (RBAC)
El sistema valida el nivel de acceso al iniciar sesión:
1. **Administrador:** Acceso total (CRUD de productos, Ventas y Usuarios).
2. **Vendedor:** Acceso restringido a consulta de stock y registro de ventas.
3. **Inventario:** Acceso a actualización de stock y carga de productos.

## 📊 Lógica de Base de Datos
- **Restricciones (Constraints):** Control de stock mínimo para evitar valores negativos.
- **Consultas Dinámicas:** Uso de `LIKE` para buscadores inteligentes de productos.
