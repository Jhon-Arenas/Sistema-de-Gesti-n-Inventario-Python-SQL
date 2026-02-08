import customtkinter as ctk
import pandas as pd
from conexion_base import conectar_bd
from tkinter import messagebox
from datetime import datetime

class SeccionReportes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.titulo = ctk.CTkLabel(self, text="📊 Reportes y Estadísticas", font=("Roboto", 24, "bold"))
        self.titulo.pack(pady=20)

        # Contenedor de "Tarjetas" informativas
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=20, pady=10)

        self.generar_reporte_resumen()

    def generar_reporte_resumen(self):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Ejemplo: Calcular Total Ventas
            cursor.execute("SELECT SUM(Cantidad_Vendida) FROM Ventas")
            total_unidades = cursor.fetchone()[0] or 0

            # Crear una tarjeta visual para el dato
            self.crear_tarjeta("Unidades Vendidas", str(total_unidades), "#2ecc71")

            conexion.close()
        except Exception as e:
            print(f"Error en reporte: {e}")

    def crear_tarjeta(self, titulo, valor, color):
        card = ctk.CTkFrame(self.cards_frame, width=200, height=100, border_width=2, border_color=color)
        card.pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(card, text=titulo, font=("Roboto", 12)).pack(pady=5)
        ctk.CTkLabel(card, text=valor, font=("Roboto", 20, "bold"), text_color=color).pack(pady=5)
    # --- BOTÓN DE EXPORTAR ---
        self.btn_exportar = ctk.CTkButton(
            self, 
            text="📥 Exportar Ventas a Excel", 
            fg_color="#1f538d", 
            hover_color="#14375e",
            command=self.exportar_a_excel
        )
        self.btn_exportar.pack(pady=30)

    def exportar_a_excel(self):
        try:
            # 1. Conectar y obtener datos
            conexion = conectar_bd()
            query = "SELECT * FROM Ventas" # Traemos toda la tabla de ventas
            
            # 2. Usar Pandas para leer la SQL
            # Esto crea un 'DataFrame', que es como una tabla de Excel en memoria
            df = pd.read_sql_query(query, conexion)
            
            if df.empty:
                messagebox.showwarning("Aviso", "No hay datos de ventas para exportar.")
                return

            # 3. Crear nombre de archivo con fecha para que no se sobrescriban
            fecha_hoy = datetime.now().strftime("%Y-%m-%d_%H-%M")
            nombre_archivo = f"Reporte_Ventas_{fecha_hoy}.xlsx"

            # 4. ¡Magia! Convertir a Excel
            df.to_excel(nombre_archivo, index=False, engine='openpyxl')
            
            conexion.close()
            messagebox.showinfo("Éxito", f"Archivo guardado como:\n{nombre_archivo}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el Excel: {e}")