import os
import sqlite3

def conectar_bd():
    try:
        # 1. Obtenemos la ruta absoluta de la carpeta donde vive el archivo
        # Esto evita que la base de datos se guarde en carpetas temporales raras
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_db = os.path.join(directorio_actual, "inventario.db")
        
        # 2. Conectamos usando la ruta completa
        conexion = sqlite3.connect(ruta_db)
        return conexion
    except Exception as e:
        print(f"❌ Error crítico al conectar con la base de datos: {e}")
        return None