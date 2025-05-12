# Este es un forrmulario que se abre cuando se quieren ingresar los datos a la hoja de ingresos
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
tittle = ctk.CTkLabel(app, text="Control de ingresos diarios", font=("Arial", 24))
tittle.pack(pady=20)


frame1 = ctk.CTkFrame(app, fg_color="transparent")
frame1.pack(pady=20)

fila_Actual = [0]

entradas = []

def agregar_fila():
    
    
    # añadir otra fila
    fila_Actual[0] += 1
    # nuevo entry 
    nueva_partida = ctk.CTkEntry(frame1, placeholder_text="Partida")
    nueva_partida.grid(row=fila_Actual[0], column=0, padx=10, pady=5)
    nuevo_resultado = ctk.CTkEntry(frame1, placeholder_text="Resultado")
    nuevo_resultado.grid(row=fila_Actual[0], column=1, padx=10, pady=5)
    
    entradas.append(nueva_partida)
    entradas.append(nuevo_resultado)
    
    # boton para recorrer el boton
    btnOK.grid(row=fila_Actual[0], column=2, padx=10, pady=10)


partida = ctk.CTkEntry(frame1, placeholder_text="Partida")
partida.grid(row=0, column=0, padx=10)
resultado = ctk.CTkEntry(frame1, placeholder_text="Resultado")
resultado.grid(row=0, column=1, padx=10)
btnOK = ctk.CTkButton(frame1, text="SI", command=agregar_fila)
btnOK.grid(row=0, column=2, padx=10)


# --- BOTONES PARA GUARDAR Y PARA GENERAR EL ARCHIVO ---
frame2 = ctk.CTkFrame(app, fg_color="transparent")
frame2.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)
btnGuardar = ctk.CTkButton(frame2, text="Guardar")
btnGuardar.grid(row=0, column=0, padx=10)
btnGenerar = ctk.CTkButton(frame2, text="Descargar")
btnGenerar.grid(row=0, column=1, padx=10)
app.mainloop()
