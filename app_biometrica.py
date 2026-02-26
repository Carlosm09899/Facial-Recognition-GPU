import customtkinter as ctk
import subprocess
import sys
import os
import sqlite3
from tkinter import messagebox

# Configuración de Refinamiento Visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

class AppBiometricaElegance(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de Ventana
        self.title("Security Management System | Management Console")
        self.geometry("1100x700")
        self.configure(fg_color="#121212") 

        # Layout: Sidebar (Control) + Workspace (Visualización)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="SECURE-ID", 
                                       font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), 
                                       text_color="#ffffff")
        self.logo_label.grid(row=0, column=0, padx=30, pady=(40, 5))
        
        self.ver_label = ctk.CTkLabel(self.sidebar, text="ENTERPRISE EDITION 2026", 
                                      font=ctk.CTkFont(size=10, weight="bold"), text_color="#666")
        self.ver_label.grid(row=1, column=0, padx=30, pady=(0, 40))

        # Botones de Acción (Corregidos)
        self.create_action_btn("Iniciar Escaneo", self.ejecutar_monitor, 2)
        self.create_action_btn("Registrar Usuario", self.solicitar_nombre_registro, 3)
        self.create_action_btn("Gestionar Bajas", self.borrar_usuario, 4)
        self.create_action_btn("Actualizar Registros", self.ver_historial, 5)

        # Módulo de Sistema
        self.sys_info = ctk.CTkFrame(self.sidebar, fg_color="#222", corner_radius=8)
        self.sys_info.grid(row=11, column=0, padx=20, pady=30, sticky="ew")
        
        ctk.CTkLabel(self.sys_info, text="ACCELERATION STATUS", font=ctk.CTkFont(size=9, weight="bold"), text_color="#3b82f6").pack(pady=(8, 0))
        ctk.CTkLabel(self.sys_info, text="RTX 3050 - ENCRYPTED", font=ctk.CTkFont(size=11)).pack(pady=(2, 8))

        # --- WORKSPACE ---
        self.workspace = ctk.CTkFrame(self, corner_radius=20, fg_color="#1e1e1e")
        self.workspace.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        self.workspace.grid_columnconfigure(0, weight=1)
        self.workspace.grid_rowconfigure(1, weight=1)

        # Encabezado (Corregido: weight="normal" para evitar el error de Tkinter)
        self.header = ctk.CTkLabel(self.workspace, text="Registro de Actividad Reciente", 
                                   font=ctk.CTkFont(size=20, weight="bold"), text_color="#f0f0f0")
        self.header.grid(row=0, column=0, sticky="w", padx=35, pady=(30, 15))

        # Visor de Historial
        self.txt_historial = ctk.CTkTextbox(self.workspace, corner_radius=12, 
                                            fg_color="#151515", border_width=1, border_color="#333",
                                            text_color="#d1d1d1", font=ctk.CTkFont(family="Segoe UI", size=13))
        self.txt_historial.grid(row=1, column=0, padx=35, pady=10, sticky="nsew")

        # Footer Actions
        self.footer = ctk.CTkFrame(self.workspace, fg_color="transparent")
        self.footer.grid(row=2, column=0, padx=35, pady=25, sticky="ew")

        self.btn_exit = ctk.CTkButton(self.footer, text="Finalizar Sesión", command=self.quit, 
                                      fg_color="#333", hover_color="#c0392b", height=35, width=120)
        self.btn_exit.pack(side="right")

        self.ver_historial()

    def create_action_btn(self, text, command, row):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, height=45, corner_radius=6,
                            fg_color="#282828", hover_color="#3b82f6", font=ctk.CTkFont(size=13))
        btn.grid(row=row, column=0, padx=25, pady=8, sticky="ew")

    def ejecutar_monitor(self):
        ruta = os.path.join(os.path.dirname(__file__), "main_access.py")
        subprocess.Popen([sys.executable, ruta])

    def solicitar_nombre_registro(self):
        dialogo = ctk.CTkInputDialog(text="Ingrese el nombre del titular:", title="Autenticación")
        nombre = dialogo.get_input()
        if nombre:
            ruta = os.path.join(os.path.dirname(__file__), "database_manager.py")
            subprocess.Popen([sys.executable, ruta, nombre])

    def borrar_usuario(self):
        dialogo = ctk.CTkInputDialog(text="Nombre del registro a eliminar:", title="Gestión de Datos")
        nombre = dialogo.get_input()
        if nombre:
            try:
                conn = sqlite3.connect('usuarios_biometria.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM rostros WHERE nombre = ?", (nombre,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Sistema", f"Acceso revocado para: {nombre}")
                else:
                    messagebox.showwarning("Sistema", "Usuario no localizado.")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Fallo en DB: {e}")

    def ver_historial(self):
        self.txt_historial.configure(state="normal")
        self.txt_historial.delete("1.0", "end")
        try:
            conn = sqlite3.connect('usuarios_biometria.db')
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, fecha FROM historial_accesos ORDER BY id DESC LIMIT 50")
            for reg in cursor.fetchall():
                self.txt_historial.insert("end", f" • [{reg[1]}]  AUTORIZADO: {reg[0].upper()}\n")
            conn.close()
        except:
            self.txt_historial.insert("end", "Conectando con el servidor de datos...")
        self.txt_historial.configure(state="disabled")

if __name__ == "__main__":
    app = AppBiometricaElegance()
    app.mainloop()