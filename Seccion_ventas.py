import customtkinter as ctk
from conexion_base import conectar_bd
from tkinter import messagebox

class SeccionVentas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent") # 'master' será el home_frame

        # Título Interno (Esto ya lo tenías, se queda igual)
        self.titulo_label = ctk.CTkLabel(self, text="Registro de Ventas", font=("Roboto", 24, "bold"))
        self.titulo_label.pack(pady=20)

        # Campos de entrada
        self.entry_id_producto = ctk.CTkEntry(self, placeholder_text="ID del Producto", width=250)
        self.entry_id_producto.pack(pady=10)

        self.entry_cantidad = ctk.CTkEntry(self, placeholder_text="Cantidad Vendida", width=250)
        self.entry_cantidad.pack(pady=10)

        self.entry_cliente = ctk.CTkEntry(self, placeholder_text="Nombre del Cliente (Opcional)", width=250)
        self.entry_cliente.pack(pady=10)

        # Combobox Método de Pago
        self.label_pago = ctk.CTkLabel(self, text="Método de Pago:")
        self.label_pago.pack(pady=(10, 0))

        self.combo_pago = ctk.CTkComboBox(
            self, 
            values=["Efectivo", "Transferencia", "Pago Móvil", "Divisas"],
            state="readonly"
        )
        self.combo_pago.pack(pady=10)
        self.combo_pago.set("Efectivo")

        # Botón Registrar
        self.btn_registrar = ctk.CTkButton(self, text="Registrar Venta", command=self.registrar_venta)
        self.btn_registrar.pack(pady=20)

        # Tabla de ventas (ahora es un CTkScrollableFrame para que se vea más profesional)
        self.tabla_ventas = ctk.CTkScrollableFrame(self, width=600, height=300, fg_color="#1a1a1a", corner_radius=10)
        self.tabla_ventas.pack(pady=10, padx=20, fill="both", expand=True)

        self.actualizar_historial() # Cargamos el historial al iniciar la sección

    def registrar_venta(self):
        # 1. Obtener datos de los componentes
        id_prod = self.entry_id_producto.get()
        cant = self.entry_cantidad.get()
        nombre_cliente = self.entry_cliente.get()
        metodo = self.combo_pago.get()

        if not id_prod or not cant:
            messagebox.showwarning("Atención", "Completa todos los campos.")
            return

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # --- PASO A: REGISTRAR LA VENTA ---
            # Incluimos el tercer parámetro: Metodo_Pago
            query_insert = "INSERT INTO Ventas (ID_Producto, Cantidad_Vendida, Nombre_Cliente, Metodo_Pago) VALUES (?, ?, ?, ?)"
            cursor.execute(query_insert, (int(id_prod), int(cant), nombre_cliente, metodo))

            # --- PASO B: RESTAR EL STOCK ---
            query_update = "UPDATE Productos SET Stock = Stock - ? WHERE ID_Producto = ?"
            cursor.execute(query_update, (int(cant), int(id_prod)))

            # Confirmar transacción
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", f"Venta registrada. Stock actualizado de ID: {id_prod}")

            # ACTUALIZAR LA TABLA DE HISTORIAL DE VENTAS
            self.actualizar_historial()
            
            # Limpiar campos para la siguiente venta
            self.entry_id_producto.delete(0, 'end')
            self.entry_cantidad.delete(0, 'end')
            self.combo_pago.set("Efectivo")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la venta: {e}")

    def actualizar_historial(self):
        for widget in self.tabla_ventas.winfo_children():
            widget.destroy()

        # Conectamos a la base de datos para obtener el historial de ventas
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            
            query = "SELECT ID_Venta, ID_Producto, Cantidad_Vendida, Nombre_Cliente, Fecha, Metodo_Pago FROM Ventas"
            cursor.execute(query)
            resultados = cursor.fetchall()

            for r in resultados:
                # 1. Crear la fila (Frame)
                fila = ctk.CTkFrame(self.tabla_ventas, fg_color="transparent")
                fila.pack(fill="x", pady=2)

                # 2. Configurar columnas del grid para que sean proporcionales
                fila.grid_columnconfigure(0, weight=1) # ID
                fila.grid_columnconfigure(1, weight=3) # Producto
                fila.grid_columnconfigure(2, weight=1) # Cant
                fila.grid_columnconfigure(3, weight=3) # Cliente
                fila.grid_columnconfigure(4, weight=4) # Fecha (Le damos más espacio)
                fila.grid_columnconfigure(5, weight=2) # Pago

                # 3. Insertar datos con grid en lugar de pack
                ctk.CTkLabel(fila, text=f"ID: {r[0]}", anchor="w").grid(row=0, column=0, padx=5)
                ctk.CTkLabel(fila, text=f"Prod: {r[1]}", anchor="w").grid(row=0, column=1, padx=5)
                ctk.CTkLabel(fila, text=f"Cant: {r[2]}").grid(row=0, column=2, padx=5)
                ctk.CTkLabel(fila, text=f"Cli: {r[3] or 'N/A'}", anchor="w").grid(row=0, column=3, padx=5)
                
                # Aquí está el truco: formateamos la fecha para que no sea tan larga
                fecha_formateada = str(r[4])[:16] # Solo YYYY-MM-DD HH:MM
                ctk.CTkLabel(fila, text=fecha_formateada).grid(row=0, column=4, padx=5)
                
                ctk.CTkLabel(fila, text=f"Modo: {r[5]}").grid(row=0, column=5, padx=5)

                # Línea divisoria
                linea = ctk.CTkFrame(self.tabla_ventas, height=1, fg_color="#333333")
                linea.pack(fill="x", padx=10, pady=2)

            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener el historial: {e}")