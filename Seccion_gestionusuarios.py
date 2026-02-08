import customtkinter as ctk
from conexion_base import conectar_bd
from tkinter import messagebox

class SeccionGestionUsuarios(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Título Interno
        self.titulo_label = ctk.CTkLabel(self, text="Gestión de Usuarios", font=("Roboto", 24, "bold"))
        self.titulo_label.pack(pady=20)

        # Campos de entrada
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre de Usuario", width=250)
        self.entry_nombre.pack(pady=10)

        self.entry_contraseña = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=250)
        self.entry_contraseña.pack(pady=10)

        # Combobox Rol
        self.label_rol = ctk.CTkLabel(self, text="Rol del Usuario:")
        self.label_rol.pack(pady=(10, 0))

        self.combo_rol = ctk.CTkComboBox(
            self, 
            values=["Administrador", "Vendedor", "Inventario"],
            state="readonly"
        )
        self.combo_rol.pack(pady=10)
        self.combo_rol.set("Vendedor")

        # Botón Guardar
        self.btn_guardar = ctk.CTkButton(self, text="Guardar Usuario", command=self.guardar_usuario)
        self.btn_guardar.pack(pady=20)

    def guardar_usuario(self):
        nombre = self.entry_nombre.get()
        contraseña = self.entry_contraseña.get()
        rol = self.combo_rol.get()

        if not nombre or not contraseña:
            messagebox.showwarning("Atención", "Completa todos los campos.")
            return

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            query = "INSERT INTO Usuarios (Nombre_Usuario, Contraseña, Rol) VALUES (?, ?, ?)"
            cursor.execute(query, (nombre, contraseña, rol))

            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", f"Usuario '{nombre}' guardado correctamente.")
            
            # Limpiar campos para un nuevo registro
            self.entry_nombre.delete(0, 'end')
            self.entry_contraseña.delete(0, 'end')
            self.combo_rol.set("Vendedor")

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo guardar el usuario: {e}")