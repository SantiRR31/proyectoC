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
tittle = ctk.CTkLabel(app, text="Sistema de control de ingresos", font=("Arial", 24))
tittle.pack(pady=20)


frame1 = ctk.CTkFrame(app, fg_color="transparent")
frame1.pack(pady=20)

partida = ctk.CTkEntry(frame1, placeholder_text="Partida")
partida.grid(row=0, column=0, padx=10)
resultado = ctk.CTkEntry(frame1, placeholder_text="Resultado")
resultado.grid(row=0, column=1, padx=10)
btnOK = ctk.CTkButton(frame1, text="SI")
btnOK.grid(row=0, column=2, padx=10)




app.mainloop()