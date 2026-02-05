import pyodbc

def conectar_bd():
    try:
        servidor = r'localhost\SQLEXPRESS'  # Cambia esto por tu servidor SQL
        base_datos = 'Emprendimiento'  # Cambia esto por el nombre de tu base de datos

        conexion = pyodbc.connect(
            'DRIVER={SQL Server};'
            f'SERVER={servidor};'
            f'DATABASE={base_datos};'
            'Trusted_Connection=yes;'
        )
        print("------------------------------------")
        print("Conexión exitosa a la base de datos.")
        print("------------------------------------")
        return conexion
    except pyodbc.Error as e:
        print("------------------------------------")
        print("Error al conectar a la base de datos:", e)
        print("------------------------------------")
        return None