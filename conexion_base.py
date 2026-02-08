import pyodbc
import sqlite3 # Importamos la librería nativa de Python

def conectar_bd():
    try:
        # Esto buscará (o creará) el archivo en la misma carpeta que el .exe
        conexion = sqlite3.connect("inventario.db") 
        return conexion
    except Exception as e:
        print(f"Error al conectar con SQLite: {e}")
        return None