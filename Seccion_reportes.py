import customtkinter as ctk
import pandas as pd
from conexion_base import conectar_bd
from tkinter import messagebox
from datetime import datetime
from tkinter import filedialog

class SeccionReportes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # 1. TÍTULO
        self.label_titulo = ctk.CTkLabel(self, text="📊 Panel de Reportes y Estadísticas", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(pady=20)

        # 2. TARJETAS DE INDICADORES (KPIs)
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cards.pack(fill="x", padx=20, pady=10)

        # Tarjeta: Ventas Totales
        self.card_total = ctk.CTkFrame(self.frame_cards, corner_radius=15)
        self.card_total.pack(side="left", padx=10, expand=True, fill="both")
        ctk.CTkLabel(self.card_total, text="Ventas Totales", font=("Roboto", 14)).pack(pady=(10,0))
        self.lbl_dinero = ctk.CTkLabel(self.card_total, text="$ 0.00", font=("Roboto", 22, "bold"), text_color="#28a745")
        self.lbl_dinero.pack(pady=10)

        # Tarjeta: Producto Estrella
        self.card_top = ctk.CTkFrame(self.frame_cards, corner_radius=15)
        self.card_top.pack(side="left", padx=10, expand=True, fill="both")
        ctk.CTkLabel(self.card_top, text="Producto Estrella", font=("Roboto", 14)).pack(pady=(10,0))
        self.lbl_producto = ctk.CTkLabel(self.card_top, text="---", font=("Roboto", 18, "bold"), text_color="#E67E22")
        self.lbl_producto.pack(pady=10)

        # 3. BARRA DE HERRAMIENTAS (Filtros y Acciones)
        self.frame_tools = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tools.pack(pady=20, padx=20, fill="x")

        self.entry_cliente = ctk.CTkEntry(self.frame_tools, placeholder_text="Filtrar por Cliente", width=200)
        self.entry_cliente.pack(side="left", padx=5)

        self.entry_fecha = ctk.CTkEntry(self.frame_tools, placeholder_text="Fecha (AAAA-MM-DD)", width=150)
        self.entry_fecha.pack(side="left", padx=5)

        self.btn_generar = ctk.CTkButton(self.frame_tools, text="🔄 Actualizar", width=100, command=self.generar_reporte)
        self.btn_generar.pack(side="left", padx=5)

        self.btn_excel = ctk.CTkButton(self.frame_tools, text="📊 Exportar Excel", fg_color="#1D6F42", 
                                        hover_color="#145A32", command=self.exportar_a_excel)
        self.btn_excel.pack(side="right", padx=5)

        # 4. LISTADO DE MOVIMIENTOS RECIENTES
        ctk.CTkLabel(self, text="Últimos Movimientos", font=("Roboto", 16, "bold")).pack(pady=5)
        self.scroll_reporte = ctk.CTkScrollableFrame(self, height=300)
        self.scroll_reporte.pack(pady=10, padx=20, fill="both", expand=True)

        # Cargar datos iniciales
        self.generar_reporte()

    def generar_reporte(self):
        for widget in self.scroll_reporte.winfo_children():
            widget.destroy()

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Suma total
            cursor.execute("SELECT SUM(Total_Venta) FROM Ventas")
            total = cursor.fetchone()[0] or 0
            self.lbl_dinero.configure(text=f"$ {total:,.2f}")

            # Top Producto
            cursor.execute("""
                SELECT Nombre_Producto, SUM(Cantidad) as total_cant 
                FROM Detalle_Ventas 
                GROUP BY id_producto 
                ORDER BY total_cant DESC LIMIT 1
            """)
            top = cursor.fetchone()
            if top:
                self.lbl_producto.configure(text=f"{top[0]} ({top[1]})")

            # Lista detallada
            cursor.execute("SELECT ID_Venta, Fecha, Nombre_Cliente, Total_Venta FROM Ventas ORDER BY Fecha DESC")
            for v in cursor.fetchall():
                fila = ctk.CTkFrame(self.scroll_reporte)
                fila.pack(fill="x", pady=2, padx=5)
                texto = f"ID: {v[0]} | 📅 {v[1][:16]} | 👤 {v[2]} | 💰 ${v[3]:.2f}"
                ctk.CTkLabel(fila, text=texto).pack(side="left", padx=10)

            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {e}")

    def exportar_a_excel(self):
        try:
            conexion = conectar_bd()
            df = pd.read_sql_query("SELECT * FROM Ventas", conexion)
            conexion.close()

            nombre_buscado = self.entry_cliente.get()
            fecha_buscada = self.entry_fecha.get()

            if nombre_buscado:
                df = df[df['Nombre_Cliente'].str.contains(nombre_buscado, case=False, na=False)]
            if fecha_buscada:
                df = df[df['Fecha'].str.contains(fecha_buscada, na=False)]

            if df.empty:
                messagebox.showwarning("Aviso", "No hay datos para exportar con esos filtros.")
                return
            
            nombre_sugerido = f"Reporte_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
            ruta_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")], initialfile=nombre_sugerido)

            if ruta_archivo:
                df.to_excel(ruta_archivo, index=False)
                messagebox.showinfo("Éxito", "¡Reporte Excel generado correctamente!")

        except Exception as e:
            messagebox.showerror("Error", f"Fallo al exportar: {e}")