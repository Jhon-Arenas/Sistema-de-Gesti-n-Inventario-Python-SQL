import customtkinter as ctk
from conexion_base import conectar_bd
from tkinter import messagebox

class SeccionVentas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.carrito = [] 

        # 1. TÍTULO PRINCIPAL
        self.titulo_label = ctk.CTkLabel(self, text="Sistema de Punto de Venta", font=("Roboto", 24, "bold"))
        self.titulo_label.pack(pady=10)

        # 2. CREACIÓN DE PESTAÑAS (Tabview)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_venta = self.tabview.add("Nueva Venta")
        self.tab_historial = self.tabview.add("Historial de Ventas")

        # --- CONFIGURACIÓN PESTAÑA: NUEVA VENTA ---
        # Contenedor para dividir Izquierda y Derecha dentro de la pestaña
        self.cont_venta = ctk.CTkFrame(self.tab_venta, fg_color="transparent")
        self.cont_venta.pack(fill="both", expand=True)

        # Panel Izquierdo: Formulario
        self.frame_datos = ctk.CTkFrame(self.cont_venta, width=300)
        self.frame_datos.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.frame_datos, text="Datos del Producto", font=("Roboto", 16, "bold")).pack(pady=10)

        self.entry_id_producto = ctk.CTkEntry(self.frame_datos, placeholder_text="ID del Producto", width=220)
        self.entry_id_producto.pack(pady=10)

        self.entry_cantidad = ctk.CTkEntry(self.frame_datos, placeholder_text="Cantidad", width=220)
        self.entry_cantidad.pack(pady=10)
        
        self.entry_cliente = ctk.CTkEntry(self.frame_datos, placeholder_text="Nombre del Cliente", width=220)
        self.entry_cliente.pack(pady=10)

        ctk.CTkLabel(self.frame_datos, text="Método de Pago:").pack(pady=(10, 0))
        self.combo_pago = ctk.CTkComboBox(self.frame_datos, values=["Efectivo", "Transferencia", "Pago Móvil", "Divisas"], state="readonly")
        self.combo_pago.pack(pady=10)
        self.combo_pago.set("Efectivo")

        self.btn_añadir = ctk.CTkButton(self.frame_datos, text="➕ Añadir al Carrito", command=self.añadir_al_carrito)
        self.btn_añadir.pack(pady=20)

        # Panel Derecho: Carrito
        self.frame_carrito = ctk.CTkFrame(self.cont_venta, fg_color="#1a1a1a")
        self.frame_carrito.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame_carrito, text="🛒 Carrito Actual", font=("Roboto", 18)).pack(pady=10)

        self.tabla_carrito = ctk.CTkScrollableFrame(self.frame_carrito, fg_color="transparent")
        self.tabla_carrito.pack(fill="both", expand=True, padx=5, pady=5)

        self.btn_vaciar = ctk.CTkButton(self.frame_carrito, text="🗑️ Vaciar Carrito", 
                                        fg_color="#dc3545", hover_color="#c82333",
                                        command=self.vaciar_carrito_accion)
        self.btn_vaciar.pack(pady=5, padx=20, fill="x")

        self.btn_finalizar = ctk.CTkButton(self.frame_carrito, text="✅ Finalizar Venta", 
                                          fg_color="#28a745", hover_color="#218838",
                                          command=self.finalizar_venta)
        self.btn_finalizar.pack(pady=15, padx=20, fill="x")

        # --- CONFIGURACIÓN PESTAÑA: HISTORIAL ---
        self.frame_historial = ctk.CTkFrame(self.tab_historial, fg_color="transparent")
        self.frame_historial.pack(fill="both", expand=True)

        self.btn_refrescar = ctk.CTkButton(self.frame_historial, text="🔄 Actualizar Historial", 
                                           command=self.actualizar_historial_pro)
        self.btn_refrescar.pack(pady=10)

        self.tabla_historial = ctk.CTkScrollableFrame(self.frame_historial, fg_color="#1a1a1a")
        self.tabla_historial.pack(fill="both", expand=True, padx=10, pady=10)

    # --- LÓGICA DE PROCESOS ---
    def añadir_al_carrito(self):
        id_p = self.entry_id_producto.get()
        cant_solicitada = self.entry_cantidad.get()

        # 1. Validación básica de campos vacíos
        if not id_p or not cant_solicitada:
            messagebox.showwarning("Faltan datos", "Por favor, ingresa ID y Cantidad.")
            return

        try:
            # Convertimos la cantidad a entero y verificamos que sea mayor a 0
            cant_solicitada = int(cant_solicitada)
            if cant_solicitada <= 0:
                messagebox.showwarning("Cantidad Inválida", "La cantidad debe ser mayor a cero.")
                return

            conexion = conectar_bd()
            cursor = conexion.cursor()
            
            # 2. Pedimos Nombre, Precio y STOCK a la base de datos
            cursor.execute("SELECT Nombre, Precio, Stock FROM Productos WHERE ID_Producto = ?", (id_p,))
            producto = cursor.fetchone()
            conexion.close()

            if producto:
                nombre, precio, stock_actual = producto
                
                # 3. EL CANDADO: Validación de Stock
                if cant_solicitada > stock_actual:
                    messagebox.showerror("Stock Insuficiente", 
                        f"¡No hay suficiente inventario!\n\nProducto: {nombre}\nStock disponible: {stock_actual}\nSolicitado: {cant_solicitada}")
                    return # Detenemos la función aquí, no se añade al carrito

                # 4. Si todo está bien, calculamos y añadimos
                subtotal = precio * cant_solicitada
                item = {
                    "id": id_p, 
                    "nombre": nombre, 
                    "cantidad": cant_solicitada, 
                    "precio": precio, 
                    "subtotal": subtotal
                }
                
                self.carrito.append(item)
                self.actualizar_vista_carrito()
                
                # Limpiamos los campos para el siguiente producto
                self.entry_id_producto.delete(0, 'end')
                self.entry_cantidad.delete(0, 'end')
                
            else:
                messagebox.showerror("Error", "Producto no encontrado en la base de datos.")

        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def actualizar_vista_carrito(self):
        for widget in self.tabla_carrito.winfo_children():
            widget.destroy()

        total = 0
        for item in self.carrito:
            fila = ctk.CTkFrame(self.tabla_carrito, fg_color="transparent")
            fila.pack(fill="x", pady=2)
            texto = f"{item['nombre']} x{item['cantidad']} - ${item['subtotal']:.2f}"
            ctk.CTkLabel(fila, text=texto).pack(side="left", padx=10)
            total += item['subtotal']

        self.titulo_label.configure(text=f"Total Carrito: ${total:.2f}")

    def vaciar_carrito_accion(self):
        if self.carrito and messagebox.askyesno("Vaciar", "¿Borrar el carrito?"):
            self.carrito = []
            self.actualizar_vista_carrito()
            self.titulo_label.configure(text="Sistema de Punto de Venta")

    def finalizar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Vacio", "El carrito está vacío.")
            return

        try:
            total_compra = sum(item['subtotal'] for item in self.carrito)
            cliente = self.entry_cliente.get() or "Consumidor Final"
            metodo = self.combo_pago.get()

            conexion = conectar_bd()
            cursor = conexion.cursor()
            
            # --- PASO 1: INSERTAR EN VENTAS (CABECERA) ---
            # Verifica que el orden coincida con tu CREATE TABLE
            cursor.execute("""INSERT INTO Ventas (id_usuario, Total_Venta, Nombre_Cliente, Metodo_Pago) 
                              VALUES (?, ?, ?, ?)""", 
                           (1, total_compra, cliente, metodo))
            
            id_v = cursor.lastrowid # Obtenemos el ID del ticket

            # --- PASO 2: DETALLES ---
            for item in self.carrito:
                cursor.execute("""INSERT INTO Detalle_Ventas (id_venta, id_producto, Nombre_Producto, Cantidad, Precio_Unitario, Subtotal) 
                                  VALUES (?, ?, ?, ?, ?, ?)""",
                               (id_v, item['id'], item['nombre'], item['cantidad'], item['precio'], item['subtotal']))
                
                # Descontar stock (lo básico por ahora)
                cursor.execute("UPDATE Productos SET Stock = Stock - ? WHERE ID_Producto = ?", 
                               (item['cantidad'], item['id']))

            conexion.commit()
            conexion.close()
            
            messagebox.showinfo("Éxito", f"Ticket #{id_v} guardado correctamente.")
            
            # Limpiar todo
            self.carrito = []
            self.actualizar_vista_carrito()
            self.entry_cliente.delete(0, 'end')
            self.actualizar_historial_pro() # ¡Para que aparezca en la otra pestaña!

        except Exception as e:
            messagebox.showerror("Error", f"Error al finalizar: {e}")

    def actualizar_historial_pro(self):
        for widget in self.tabla_historial.winfo_children():
            widget.destroy()

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT ID_Venta, Fecha, Total_Venta, Nombre_Cliente FROM Ventas ORDER BY ID_Venta DESC")
            for r in cursor.fetchall():
                fila = ctk.CTkFrame(self.tabla_historial, fg_color="#2b2b2b")
                fila.pack(fill="x", pady=5, padx=5)
                info = f"Ticket #{r[0]} | {r[1][:16]} | Cli: {r[3]} | Total: ${r[2]:.2f}"
                ctk.CTkLabel(fila, text=info).pack(side="left", padx=10)
            conexion.close()
        except Exception as e:
            print(f"Error cargando historial: {e}")