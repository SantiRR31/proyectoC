# Interfaz principal al lanzar el programa
import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("light")  # Modes: "system" (default), "light", "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

app = ctk.CTk()  
app.geometry("400x300")
app.title("Programa")



app.mainloop()