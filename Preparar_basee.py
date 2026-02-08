import sqlite3

def crear_tablas():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    # Tabla Productos
    cursor.execute('''CREATE TABLE IF NOT EXISTS Productos (
        ID_Producto INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Stock INTEGER DEFAULT 0,
        Precio REAL DEFAULT 0.0
    )''')

    # Tabla Ventas (con Nombre_Cliente y Metodo_Pago como pediste)
    cursor.execute('''CREATE TABLE IF NOT EXISTS Ventas (
        ID_Venta INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Producto INTEGER,
        Cantidad_Vendida INTEGER,
        Metodo_Pago TEXT,
        Nombre_Cliente TEXT,
        Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ID_Producto) REFERENCES Productos (ID_Producto)
    )''')

    # Tabla Usuarios (para tu Login)
    cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios (
        ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre_Usuario TEXT UNIQUE,
        Contraseña TEXT,
        Rol TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre_Usuario TEXT UNIQUE NOT NULL,
        Contraseña TEXT NOT NULL,
        Rol TEXT NOT NULL  -- Aquí pondremos 'Admin' o 'Empleado'
    )
''')

    # Creamos tu usuario Maestro
    # ¡IMPORTANTE: Tú serás el 'Admin'!
    cursor.execute('''
    INSERT OR IGNORE INTO Usuarios (Nombre_Usuario, Contraseña, Rol) 
    VALUES (?, ?, ?)
''', ("Rick", "tu_clave_secreta", "Admin"))

    # Insertar tu usuario inicial para que puedas entrar
    try:
        cursor.execute("INSERT INTO Usuarios (Nombre_Usuario, Contraseña, Rol) VALUES (?, ?, ?)", 
                       ('Rick', '1234', 'Administrador'))
    except:
        pass # Por si ya existe

    conexion.commit()
    conexion.close()
    print("Base de datos SQLite lista para ser portable.")

if __name__ == "__main__":
    crear_tablas()