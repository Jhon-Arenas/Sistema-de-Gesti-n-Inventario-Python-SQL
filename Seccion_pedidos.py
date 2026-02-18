import customtkinter as ctk
from conexion_base import conectar_bd
from tkinter import messagebox

class SeccionPedidos (ctk.CTkFrame):
    def __init__(self, master) :
        super().__init__(master, fg_color="transparent")

        # Variables para capturar datos
        self.var_cliente = ctk.StringVar()
        self.var_producto = ctk.StringVar()
        self.var_cantidad = ctk.StringVar()

        # Título de la sección
        self.lbl_titulo = ctk.CTkLabel(self, text="📝 Registro de Pedidos Pendientes", font=("Roboto", 24, "bold"))
        self.lbl_titulo.pack(pady=20)

        # --- AQUÍ DEBERÍAS CREAR EL FORMULARIO ---
        # Creamos un marco para agrupar los campos de entrada
        self.frame_formulario = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        self.frame_formulario.pack(fill="x", padx=40, pady=10)

        # Campo: Nombre del Cliente
        # Campo: Nombre del Cliente
        self.entry_cliente = ctk.CTkEntry(
            self.frame_formulario, 
            placeholder_text="Nombre del cliente...", # <-- ¡Ahora sí se verá!
            width=200
        )
        self.entry_cliente.pack(side="left", padx=10, pady=20)

        # Campo: Producto
        self.entry_producto = ctk.CTkEntry(
            self.frame_formulario, 
            placeholder_text="¿Qué producto quiere?", 
            width=200
        )
        self.entry_producto.pack(side="left", padx=10, pady=20)

        # Campo: Cantidad
        self.entry_cantidad = ctk.CTkEntry(
            self.frame_formulario, 
            placeholder_text="Cantidad", 
            width=100
        )
        self.entry_cantidad.pack(side="left", padx=10, pady=20)

        # Botón para Registrar
        self.btn_registrar = ctk.CTkButton(
            self, 
            text="➕ Registrar Pedido", 
            command=self.registrar_pedido, # <--- Llamará a la función que haremos
            fg_color="#27ae60", 
            hover_color="#2ecc71"
        )
        self.btn_registrar.pack(pady=20)

        # --- CABECERA DE LA TABLA ---
        self.frame_header = ctk.CTkFrame(self, fg_color="#333333", corner_radius=5)
        self.frame_header.pack(fill="x", padx=40, pady=(10, 0))

        # Definimos anchos fijos para que todo cuadre
        columnas = [("ID", 50), ("Cliente", 150), ("Producto", 150), ("Cant.", 80), ("Estado", 100), ("Acción", 120)]
        
        for texto, ancho in columnas:
            lbl = ctk.CTkLabel(self.frame_header, text=texto, width=ancho, font=("Roboto", 12, "bold"))
            lbl.pack(side="left", padx=5)

        # --- CUERPO DE LA TABLA (Scrollable) ---
        self.tabla_pedidos = ctk.CTkScrollableFrame(self, width=700, height=300, fg_color="transparent")
        self.tabla_pedidos.pack(pady=(0, 20), padx=40, fill="both", expand=True)

        self.actualizar_lista_pedidos()

        # --- PANEL DE ACCIONES ---
        self.frame_acciones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_acciones.pack(pady=10)

        self.entry_id_completar = ctk.CTkEntry(self.frame_acciones, placeholder_text="ID Pedido", width=80)
        self.entry_id_completar.pack(side="left", padx=10)

        self.btn_entregado = ctk.CTkButton(
            self.frame_acciones, 
            text="✔️ Marcar Entregado", 
            command=self.completar_pedido,
            fg_color="#2980b9",
            width=150
        )
        self.btn_entregado.pack(side="left", padx=10)

    # 2. Ahora, agrega la función que falta:
    def actualizar_lista_pedidos(self):
        # Limpiar la tabla anterior
        for widget in self.tabla_pedidos.winfo_children():
            widget.destroy()

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Pedidos WHERE estado = 'Pendiente'")
            filas = cursor.fetchall()

            for fila in filas:
                # Creamos un marco para la fila
                f_row = ctk.CTkFrame(self.tabla_pedidos, fg_color="gray25", height=40)
                f_row.pack(fill="x", pady=2, padx=5)

                # Datos de la fila
                ctk.CTkLabel(f_row, text=fila[0], width=50).pack(side="left", padx=5)
                ctk.CTkLabel(f_row, text=fila[1], width=150, anchor="w").pack(side="left", padx=5)
                ctk.CTkLabel(f_row, text=fila[2], width=150, anchor="w").pack(side="left", padx=5)
                ctk.CTkLabel(f_row, text=fila[3], width=80).pack(side="left", padx=5)
                
                # Estado con colorcito
                lbl_estado = ctk.CTkLabel(f_row, text=fila[4], width=100, text_color="#E67E22", font=("Roboto", 11, "bold"))
                lbl_estado.pack(side="left", padx=5)

                # BOTÓN DE ACCIÓN DIRECTO EN LA FILA
                btn_check = ctk.CTkButton(f_row, text="✔️ Entregar", width=100, height=25,
                                          fg_color="#27ae60", hover_color="#219150",
                                          command=lambda p=fila[0]: self.completar_pedido_directo(p))
                btn_check.pack(side="right", padx=10)

            conexion.close()
        except Exception as e:
            print(f"Error al construir tabla: {e}")

    def registrar_pedido(self):
        # 1. LEER DIRECTAMENTE DE LOS ENTRYS (Ya no de las variables)
        nombre = self.entry_cliente.get()
        prod = self.entry_producto.get()
        cant = self.entry_cantidad.get()

        # 2. Validación (Importante: .get() devuelve un string vacío "" si no hay nada)
        if not nombre.strip() or not prod.strip() or not cant.strip():
            print("¡Error! Faltan datos") 
            messagebox.showwarning("Atención", "Por favor, completa todos los campos.")
            return

        try:
            conexion = conectar_bd() 
            cursor = conexion.cursor()

            query = "INSERT INTO Pedidos (cliente, producto, cantidad, estado) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (nombre, prod, int(cant), "Pendiente"))

            conexion.commit()
            conexion.close() 
            
            print(f"✅ Pedido de {nombre} guardado.")

            # 3. LIMPIAR LOS CUADROS (Como ya no hay StringVars, usamos delete)
            self.entry_cliente.delete(0, 'end')
            self.entry_producto.delete(0, 'end')
            self.entry_cantidad.delete(0, 'end')

            # 4. Actualizar la lista visual y el Badge del Main
            self.actualizar_lista_pedidos()
            
            if hasattr(self.master.master, 'actualizar_badge_pedidos'):
                self.master.master.actualizar_badge_pedidos()

        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def crear_tabla_pedidos(self):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            # Esta orden crea la tabla solo si no existe ya
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Pedidos (
                    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente TEXT NOT NULL,
                    producto TEXT NOT NULL,
                    cantidad INTEGER,
                    estado TEXT NOT NULL
                )
            ''')
            conexion.commit()
            conexion.close()
        except Exception as e:
            print(f"Error al crear tabla: {e}")

    def completar_pedido_directo(self, id_ped):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # 1. Primero: Buscamos qué producto y qué cantidad tiene ese pedido
            cursor.execute("SELECT producto, cantidad FROM Pedidos WHERE id_pedido = ?", (id_ped,))
            resultado = cursor.fetchone()

            if resultado:
                nombre_producto, cantidad_pedida = resultado[0], resultado[1]

                # 2. Intentamos restar esa cantidad de la tabla de PRODUCTOS
                # Nota: Asegúrate de que tu tabla de productos se llame 'Productos' y la columna de stock 'Cantidad'
                cursor.execute("""
                    UPDATE Productos 
                    SET Cantidad = Cantidad - ? 
                    WHERE Nombre_Producto = ? AND Cantidad >= ?
                """, (cantidad_pedida, nombre_producto, cantidad_pedida))

                # Verificamos si se actualizó algún producto (si había stock suficiente)
                if cursor.rowcount == 0:
                    messagebox.showwarning("Stock Insuficiente", 
                        f"No hay suficiente stock de '{nombre_producto}' para completar este pedido.")
                    conexion.close()
                    return

                # 3. Si hubo stock, entonces sí marcamos el pedido como Entregado
                cursor.execute("UPDATE Pedidos SET estado = 'Entregado' WHERE id_pedido = ?", (id_ped,))
                
                conexion.commit()
                messagebox.showinfo("Éxito", f"Pedido {id_ped} entregado e inventario actualizado.")
            
            conexion.close()
            
            # Actualizamos la interfaz
            self.actualizar_lista_pedidos()
            if hasattr(self.master.master, 'actualizar_badge_pedidos'):
                self.master.master.actualizar_badge_pedidos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la entrega: {e}")

    def completar_pedido(self):
        id_ped = self.entry_id_completar.get()
        if not id_ped:
            messagebox.showwarning("Atención", "Escribe el ID del pedido.")
            return
        
        # En lugar de repetir código, llamamos a la función inteligente que ya hiciste
        self.completar_pedido_directo(id_ped)
        self.entry_id_completar.delete(0, 'end')


