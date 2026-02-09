import customtkinter as ctk
import pandas as pd
from conexion_base import conectar_bd
from tkinter import messagebox
from datetime import datetime
from tkinter import filedialog

class SeccionReportes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # 1. Título y Tarjetas
        self.titulo = ctk.CTkLabel(self, text="📊 Reportes y Estadísticas", font=("Roboto", 24, "bold"))
        self.titulo.pack(pady=20)

        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=20, pady=10)
        self.generar_reporte_resumen()

        # 2. Botón de Configuración de Filtros
        self.btn_config_filtros = ctk.CTkButton(
            self, text="🔍 Filtros Avanzados", 
            command=self.toggle_filtros,
            fg_color="#34495e"
        )
        self.btn_config_filtros.pack(pady=10)

        # 3. Panel de Filtros (Oculto)
        self.frame_filtros = ctk.CTkFrame(self, fg_color="gray25", corner_radius=10)
        self.entry_cliente = ctk.CTkEntry(self.frame_filtros, placeholder_text="Nombre del cliente...")
        self.entry_cliente.pack(side="left", padx=10, pady=10)
        self.entry_fecha = ctk.CTkEntry(self.frame_filtros, placeholder_text="AAAA-MM-DD")
        self.entry_fecha.pack(side="left", padx=10, pady=10)
        
        self.filtros_visibles = False 

        # 4. ÚNICO Botón de Exportar
        self.btn_exportar = ctk.CTkButton(
            self, text="📥 Exportar a Excel", 
            command=self.exportar_a_excel,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.btn_exportar.pack(pady=30)

    def generar_reporte_resumen(self):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT SUM(Cantidad_Vendida) FROM Ventas")
            total_unidades = cursor.fetchone()[0] or 0
            self.crear_tarjeta("Unidades Vendidas", str(total_unidades), "#2ecc71")
            conexion.close()
        except Exception as e:
            print(f"Error en reporte: {e}")

    def crear_tarjeta(self, titulo, valor, color):
        card = ctk.CTkFrame(self.cards_frame, width=200, height=100, border_width=2, border_color=color)
        card.pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(card, text=titulo, font=("Roboto", 12)).pack(pady=5)
        ctk.CTkLabel(card, text=valor, font=("Roboto", 20, "bold"), text_color=color).pack(pady=5)
        # AQUÍ HABÍA UN BOTÓN EXTRA, ¡LO ELIMINAMOS!

    def toggle_filtros(self):
        if not self.filtros_visibles:
            self.frame_filtros.pack(fill="x", padx=20, pady=10, after=self.btn_config_filtros)
            self.btn_config_filtros.configure(text="🔼 Cerrar Filtros")
            self.filtros_visibles = True
        else:
            self.frame_filtros.pack_forget()
            self.btn_config_filtros.configure(text="🔍 Filtros Avanzados")
            self.filtros_visibles = False

    def exportar_a_excel(self):
        try:
            conexion = conectar_bd()
            df = pd.read_sql_query("SELECT * FROM Ventas", conexion)
            conexion.close()

            nombre_buscado = self.entry_cliente.get()
            fecha_buscada = self.entry_fecha.get()

            # Filtramos por nombre si hay texto
            if nombre_buscado:
                df = df[df['Nombre_Cliente'].str.contains(nombre_buscado, case=False, na=False)]
                
            # Filtramos por fecha si hay texto
            if fecha_buscada:
                df = df[df['Fecha'].str.contains(fecha_buscada, na=False)]

            # Si el resultado está vacío, avisamos y salimos
            if df.empty:
                messagebox.showwarning("Aviso", "No se encontraron datos con esos filtros.")
                return
            
            # Preparamos el nombre con la fecha actual
            fecha_sugerida = datetime.now().strftime("%Y-%m-%d_%H-%M")
            nombre_sugerido = f"Reporte_{fecha_sugerida}.xlsx"

            # Abrimos la ventana de "Guardar como"
            ruta_archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("Todos los archivos", "*.*")],
                initialfile=nombre_sugerido,
                title="Selecciona dónde guardar tu reporte"
            )

            # Solo si el usuario eligió una ruta (no canceló), guardamos
            if ruta_archivo:
                df.to_excel(ruta_archivo, index=False)
                messagebox.showinfo("Éxito", f"Reporte guardado en:\n{ruta_archivo}")

        except Exception as e:
            messagebox.showerror("Error", f"Error en Pandas: {e}")
