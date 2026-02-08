import customtkinter as ctk
from conexion_base import conectar_bd
from tkinter import messagebox

class SeccionProductos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # --- CABECERA Y BUSCADOR ---
        self.titulo = ctk.CTkLabel(self, text="📦 Control de Inventario", font=("Roboto", 24, "bold"))
        self.titulo.pack(pady=10)

         # Frame para la búsqueda
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(pady=10, fill="x", padx=20)

        self.entry_busqueda = ctk.CTkEntry(self.search_frame, placeholder_text="🔍 Buscar producto por nombre...", width=400)
        self.entry_busqueda.pack(side="left", padx=10)
        # 🚀 El "Truco": Cada vez que escribes, filtra
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self.actualizar_tabla())

        # --- DISEÑO DE TABLA PROFESIONAL ---
        # Contenedor para la tabla
        self.tabla_container = ctk.CTkScrollableFrame(self, fg_color="#1e1e1e", corner_radius=10)
        self.tabla_container.pack(expand=True, fill="both", padx=20, pady=10)

        # Encabezados (Headers)
        self.crear_encabezado()
        
        # Cargar datos iniciales
        self.actualizar_tabla()

    def crear_encabezado(self):
        header_frame = ctk.CTkFrame(self.tabla_container, fg_color="#333333", corner_radius=0)
        header_frame.pack(fill="x")
        
        headers = [("ID", 50), ("PRODUCTO", 200), ("STOCK", 80), ("PRECIO", 100), ("ESTADO", 120)]
        for texto, ancho in headers:
            lbl = ctk.CTkLabel(header_frame, text=texto, width=ancho, font=("Roboto", 12, "bold"))
            lbl.pack(side="left", padx=5, pady=5)

    def actualizar_tabla(self):
        # Limpiar filas anteriores (menos el encabezado)
        for widget in self.tabla_container.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget.cget("fg_color") != "#333333":
                widget.destroy()

        termino = self.entry_busqueda.get()

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            
            # Buscamos por nombre usando LIKE para el filtro inteligente
            query = "SELECT ID_Producto, Nombre, Stock, Precio FROM Productos WHERE Nombre LIKE ?"
            cursor.execute(query, ('%' + termino + '%',))
            resultados = cursor.fetchall()

            for r in resultados:
                # Crear una "fila" elegante
                fila = ctk.CTkFrame(self.tabla_container, fg_color="transparent")
                fila.pack(fill="x", pady=2)
                
                # Determinar estado de stock
                color_texto = "#FFFFFF"
                status_text = "✅ Ok"
                if r[2] < 5:
                    color_texto = "#FF4444"
                    status_text = "⚠️ Bajo Stock"

                # Insertar los datos en la fila
                ctk.CTkLabel(fila, text=r[0], width=50).pack(side="left", padx=5)
                ctk.CTkLabel(fila, text=r[1], width=200, anchor="w").pack(side="left", padx=5)
                ctk.CTkLabel(fila, text=r[2], width=80, text_color=color_texto).pack(side="left", padx=5)
                ctk.CTkLabel(fila, text=f"${r[3]:.2f}", width=100).pack(side="left", padx=5)
                ctk.CTkLabel(fila, text=status_text, width=120, text_color=color_texto).pack(side="left", padx=5)

                # Línea divisoria sutil
                linea = ctk.CTkFrame(self.tabla_container, height=1, fg_color="#333333")
                linea.pack(fill="x", padx=10)

            conexion.close()
        except Exception as e:
            print(f"Error: {e}")    