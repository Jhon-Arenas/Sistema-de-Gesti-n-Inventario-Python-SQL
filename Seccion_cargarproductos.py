import customtkinter as ctk
from conexion_base import conectar_bd
from tkinter import messagebox

class SeccionCargarProductos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Título Interno
        self.titulo_label = ctk.CTkLabel(self, text="Cargar Nuevo Producto", font=("Roboto", 24, "bold"))
        self.titulo_label.pack(pady=20)

        # Campos de entrada
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre del Producto", width=250)
        self.entry_nombre.pack(pady=10)

        self.entry_stock = ctk.CTkEntry(self, placeholder_text="Stock Inicial", width=250)
        self.entry_stock.pack(pady=10)

        self.entry_precio = ctk.CTkEntry(self, placeholder_text="Precio Unitario", width=250)
        self.entry_precio.pack(pady=10)

        # --- AQUÍ ESTABA EL ERROR ---
        # Creamos un frame nuevo SOLO para los botones, para que no dependa de 'search_frame'
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        # Botón Reponer (Ahora su padre es self.frame_botones)
        self.btn_reponer = ctk.CTkButton(self.frame_botones, text="+ Reponer Stock", 
                                         width=120, fg_color="#1f538d", 
                                         command=self.abrir_reposicion_stock)
        self.btn_reponer.pack(side="left", padx=10)

        # Botón Guardar (Ahora su padre también es self.frame_botones)
        self.btn_guardar = ctk.CTkButton(self.frame_botones, text="Guardar Producto", 
                                         command=self.guardar_producto)
        self.btn_guardar.pack(side="left", padx=10)

    def guardar_producto(self):
        nombre = self.entry_nombre.get()
        stock = self.entry_stock.get()
        precio = self.entry_precio.get()

        if not nombre or not stock or not precio:
            messagebox.showwarning("Atención", "Completa todos los campos.")
            return

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            query = "INSERT INTO Productos (Nombre, Stock, Precio) VALUES (?, ?, ?)"
            cursor.execute(query, (nombre, int(stock), float(precio)))

            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", f"Producto '{nombre}' guardado correctamente.")
            
            # Limpiar campos para un nuevo registro
            self.entry_nombre.delete(0, 'end')
            self.entry_stock.delete(0, 'end')
            self.entry_precio.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo guardar el producto: {e}")

    def abrir_reposicion_stock(self):
        # Importante: Le pasamos 'self' para que la ventanita sepa quién la abrió
        ventana_reposicion = VentanaReposicionStock(master=self, ReposiciónStock="Reposición de Stock")
        ventana_reposicion.focus()