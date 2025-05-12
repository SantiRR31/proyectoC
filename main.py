# Interfaz principal al lanzar el programa
# Este archivo contiene la interfaz gráfica del programa
# Importar las librerías necesarias
# Importar las librerías necesarias
# Importar las librerías necesarias
# Importar las librerías necesarias
# Importar las librerías necesarias        
import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("light")  # Modes: "system" (default), "light", "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

icon_path = ("assets/cecati-122.ico")

app = ctk.CTk()  
app.geometry("720x480")
app.title("Programa")
app.iconbitmap(icon_path)

# --- INTERFAZ PRINCIPAL ---
tittle = ctk.CTkLabel(app, text="Sistema de Control de Asistencia", font=("Arial", 24))
tittle.pack(pady=20)


app.mainloop()