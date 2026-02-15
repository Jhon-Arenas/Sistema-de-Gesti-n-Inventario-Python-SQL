import customtkinter as ctk
import pandas as pd
from conexion_base import conectar_bd
from tkinter import messagebox

class SeccionInventario(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # 1. Título
        self.titulo = ctk.CTkLabel(self, text="📦 Gestión de Inventario", font=("Roboto", 24, "bold"))
        self.titulo.pack(pady=20)

        # 2. El Tabview
        self.tabview = ctk.CTkTabview(self, width=600, corner_radius=10)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)

        self.tabview.add("Stock Actual")
        self.tabview.add("Gestionar Producto")
        self.tabview.add("Alertas")

        # LLAMADAS A LAS FUNCIONES
        self.setup_pestana_stock()   
        self.setup_pestana_gestion() 
        self.setup_pestana_alertas()

    # --- PESTAÑA 1: STOCK ACTUAL (PROFESIONAL) ---
    def setup_pestana_stock(self):
        tab = self.tabview.tab("Stock Actual")
        
        # 1. Barra superior de control (Buscador + Botón)
        frame_control = ctk.CTkFrame(tab, fg_color="transparent")
        frame_control.pack(fill="x", padx=10, pady=10)

        # La barra de búsqueda
        self.entry_busqueda = ctk.CTkEntry(frame_control, placeholder_text="🔍 Buscar producto por nombre...", width=300)
        self.entry_busqueda.pack(side="left", padx=5)
        
        # CONEXIÓN DINÁMICA: Cada vez que escribas, se llama a la función de filtrar
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_inventario_tiempo_real)

        self.btn_refrescar = ctk.CTkButton(frame_control, text="🔄", width=40,
                                           command=self.mostrar_inventario_pro)
        self.btn_refrescar.pack(side="right")

        header_frame = ctk.CTkFrame(tab, fg_color="gray20", height=30)
        header_frame.pack(fill="x", padx=10)
        
        ctk.CTkLabel(header_frame, text="ID", width=50).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="PRODUCTO", width=200).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="STOCK", width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="PRECIO", width=100).pack(side="left", padx=5)

        self.scroll_inventario = ctk.CTkScrollableFrame(tab, fg_color="transparent", height=300)
        self.scroll_inventario.pack(fill="both", expand=True, padx=10, pady=5)

    # --- PESTAÑA 2: GESTIONAR (TU LÓGICA DE CARGA) ---
    def setup_pestana_gestion(self):
        tab = self.tabview.tab("Gestionar Producto")
        ctk.CTkLabel(tab, text="Cargar Nuevo Producto", font=("Roboto", 18, "bold")).pack(pady=15)

        self.entry_nombre = ctk.CTkEntry(tab, placeholder_text="Nombre del Producto", width=300)
        self.entry_nombre.pack(pady=10)
        self.entry_stock = ctk.CTkEntry(tab, placeholder_text="Stock Inicial", width=300)
        self.entry_stock.pack(pady=10)
        self.entry_precio = ctk.CTkEntry(tab, placeholder_text="Precio Unitario", width=300)
        self.entry_precio.pack(pady=10)

        self.frame_botones = ctk.CTkFrame(tab, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        self.btn_añadir = ctk.CTkButton(self.frame_botones, text="+ Añadir", fg_color="#0A98A0", command=self.guardar_producto)
        self.btn_añadir.pack(side="left", padx=10)

    # --- PESTAÑA 3: ALERTAS (PROFESIONAL) ---
    def setup_pestana_alertas(self):
        tab = self.tabview.tab("Alertas")
        ctk.CTkLabel(tab, text="⚠️ Productos con Stock Crítico (< 5 unidades)", font=("Roboto", 18, "bold"), text_color="#e74c3c").pack(pady=10)
        
        self.btn_check_alertas = ctk.CTkButton(tab, text="🔍 Revisar Estado Crítico", fg_color="#e67e22", command=self.mostrar_alertas_pandas)
        self.btn_check_alertas.pack(pady=10)

        self.scroll_alertas = ctk.CTkScrollableFrame(tab, fg_color="transparent", height=250, border_color="#e74c3c", border_width=1)
        self.scroll_alertas.pack(fill="both", expand=True, padx=10, pady=5)

    # --- MÉTODOS DE LÓGICA (PANDAS Y DB) ---
    def filtrar_inventario_tiempo_real(self, event):
        texto_busqueda = self.entry_busqueda.get().lower()

        try:
            # 1. Obtenemos los datos actuales de la DB
            conexion = conectar_bd()
            df = pd.read_sql_query("SELECT ID_Producto, Nombre, Stock, Precio FROM Productos", conexion)
            conexion.close()

            # 2. FILTRADO MÁGICO DE PANDAS
            # Buscamos coincidencias en la columna 'Nombre', ignorando mayúsculas
            df_filtrado = df[df['Nombre'].str.lower().str.contains(texto_busqueda)]

            # 3. Dibujamos solo los resultados filtrados
            self.actualizar_lista_visual(df_filtrado)

        except Exception as e:
            print(f"Error al filtrar: {e}")

    def actualizar_lista_visual(self, dataframe):
        for widget in self.scroll_inventario.winfo_children():
            widget.destroy()

        for _, fila in dataframe.iterrows():
            row = ctk.CTkFrame(self.scroll_inventario, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            # ✅ CORRECCIÓN AQUÍ: Cambiamos 'ID' por 'ID_Producto'
            id_val = fila['ID_Producto'] 
            
            ctk.CTkLabel(row, text=str(id_val), width=50).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=fila['Nombre'], width=200, anchor="w").pack(side="left", padx=5)
            
            color_stock = "#e74c3c" if fila['Stock'] < 5 else "white"
            ctk.CTkLabel(row, text=str(fila['Stock']), width=100, text_color=color_stock).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"${float(fila['Precio']):.2f}", width=100).pack(side="left", padx=5)
            
            ctk.CTkFrame(self.scroll_inventario, height=1, fg_color="gray30").pack(fill="x")

        # Dibujar filas del dataframe recibido
        for _, fila in dataframe.iterrows():
            row = ctk.CTkFrame(self.scroll_inventario, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=str(fila['ID']), width=50).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=fila['Nombre'], width=200, anchor="w").pack(side="left", padx=5)
            
            color_stock = "#e74c3c" if fila['Stock'] < 5 else "white"
            ctk.CTkLabel(row, text=str(fila['Stock']), width=100, text_color=color_stock).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"${float(fila['Precio']):.2f}", width=100).pack(side="left", padx=5)
            
            ctk.CTkFrame(self.scroll_inventario, height=1, fg_color="gray30").pack(fill="x")

    def mostrar_inventario_pro(self):
        # 1. Limpiar el contenedor
        for widget in self.scroll_inventario.winfo_children():
            widget.destroy()

        try:
            conexion = conectar_bd()
            # IMPORTANTE: Asegúrate de que los nombres aquí coincidan con tu DB
            df = pd.read_sql_query("SELECT ID_Producto, Nombre, Stock, Precio FROM Productos", conexion)
            conexion.close()

            # 2. Iterar sobre el DataFrame
            for index, fila in df.iterrows():
                row = ctk.CTkFrame(self.scroll_inventario, fg_color="transparent")
                row.pack(fill="x", pady=2)
                
                # --- ACCESO SEGURO POR NOMBRE ---
                # Usamos fila['NombreColumna'] que es lo estándar en Pandas
                id_val = fila['ID_Producto']
                nombre_val = fila['Nombre']
                stock_val = fila['Stock']
                precio_val = fila['Precio']

                # 3. Crear las etiquetas visuales
                ctk.CTkLabel(row, text=str(id_val), width=50).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=str(nombre_val), width=200, anchor="w").pack(side="left", padx=5)
                
                # Lógica de color para el Stock
                color_stock = "#e74c3c" if stock_val < 5 else "white"
                ctk.CTkLabel(row, text=str(stock_val), width=100, text_color=color_stock).pack(side="left", padx=5)
                
                # Formato de moneda para el Precio
                ctk.CTkLabel(row, text=f"${float(precio_val):.2f}", width=100).pack(side="left", padx=5)
                
                # Línea separadora
                ctk.CTkFrame(self.scroll_inventario, height=1, fg_color="gray30").pack(fill="x")

        except Exception as e:
            messagebox.showerror("Error de Datos", f"No se pudo cargar la tabla.\nDetalle: {e}")
            # Esto imprimirá en consola las columnas para que tú y yo las veamos
            print(f"Error detectado: {e}")

    def mostrar_alertas_pandas(self):
        # Limpiar scroll de alertas
        for widget in self.scroll_alertas.winfo_children():
            widget.destroy()

        try:
            conexion = conectar_bd()
            df = pd.read_sql_query("SELECT * FROM Productos", conexion)
            conexion.close()

            # FILTRO PANDAS: Solo lo que tenga menos de 5
            criticos = df[df['Stock'] < 5]

            if criticos.empty:
                ctk.CTkLabel(self.scroll_alertas, text="✅ Todo en orden. No hay stock bajo.").pack(pady=20)
            else:
                for _, fila in criticos.iterrows():
                    f = ctk.CTkFrame(self.scroll_alertas, fg_color="#3b201d") # Fondo rojizo sutil
                    f.pack(fill="x", pady=2, padx=5)
                    ctk.CTkLabel(f, text=f"⚠️ {fila['Nombre']}", width=250, anchor="w", text_color="#ff7675").pack(side="left", padx=10)
                    ctk.CTkLabel(f, text=f"Quedan: {fila['Stock']}", font=("Roboto", 12, "bold")).pack(side="right", padx=10)

        except Exception as e:
            messagebox.showerror("Error", f"{e}")

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
            messagebox.showinfo("Éxito", f"Producto '{nombre}' guardado.")
            self.entry_nombre.delete(0, 'end'); self.entry_stock.delete(0, 'end'); self.entry_precio.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"{e}")