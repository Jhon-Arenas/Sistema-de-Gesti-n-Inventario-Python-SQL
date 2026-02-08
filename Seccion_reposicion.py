import customtkinter as ctk
from conexion_base import conectar_bd
from tkinter import messagebox

class VentanaReposicionStock(ctk.CTkToplevel):
    def __init__(self, master, ReposiciónStock): # Agregamos 'master'
        super().__init__(master)
        self.master = master
        self.title(ReposiciónStock)
        self.geometry("400x300")
        self.attributes("-topmost", True)

        #Titulo Interno
        self.titulo_label = ctk.CTkLabel(self, text="Reposición de Stock", font=("Roboto", 20, "bold"))
        self.titulo_label.pack(pady=(20, 10))

        #Campo: ID Producto
        self.entry_id_producto = ctk.CTkEntry(self, placeholder_text="ID del Producto", width=250)
        self.entry_id_producto.pack(pady=10)

        #Campo: Cantidad a Reponer
        self.entry_cantidad = ctk.CTkEntry(self, placeholder_text="Cantidad a Reponer", width=250)
        self.entry_cantidad.pack(pady=10)

        #Botón: Reponer Stock
        self.btn_reponer = ctk.CTkButton(self, text="Reponer Stock", command=self.reponer_stock)
        self.btn_reponer.pack(pady=20)

    def reponer_stock(self):
        # 1. Obtenemos los datos de los Entries
        id_producto = self.entry_id_producto.get()
        cantidad = self.entry_cantidad.get()

        # Validación simple: que no haya campos vacíos
        if not id_producto or not cantidad:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        try:
            # 2. Conectamos (usamos tu archivo conexion_base)
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # 3. La sentencia SQL (Usamos '?' para evitar hackeos/errores)
            query = "UPDATE Productos SET Stock = Stock + ? WHERE ID_Producto = ?"
            cursor.execute(query, (int(cantidad), int(id_producto)))

            # 4. Guardar cambios y cerrar
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", f"Stock del producto ID '{id_producto}' reponido correctamente.")
            
            # Limpiar los campos para una nueva reposición
            self.entry_id_producto.delete(0, 'end')
            self.entry_cantidad.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo reponer el stock: {e}")