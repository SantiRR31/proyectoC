# Este es un forrmulario que se abre cuando se quieren ingresar los datos a la hoja de ingresos
import tkinter as tk
import customtkinter as ctk
import xlwings as xw
import sqlite3

ctk.set_appearance_mode("light")  # Modes: "system" (default), "light", "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

icon_path = ("../assets/cecati-122.ico")

app = ctk.CTk()  
app.geometry("720x480")
app.title("Programa")
app.iconbitmap(icon_path)

app.bind("<Return>", lambda event: agregar_fila_buscar())  # Presiona Enter para agregar una fila

# --- INTERFAZ PRINCIPAL ---
tittle = ctk.CTkLabel(app, text="Poliza de ingresos", font=("Arial", 24))
tittle.pack(pady=20)


frame1 = ctk.CTkFrame(app, fg_color="transparent")
frame1.pack(pady=20)

fila_Actual = [0]
entradas = []

def buscar_denominacion_db(clave):
    conn = sqlite3.connect('../prueba.db')
    cursor = conn.cursor()
    cursor.execute("SELECT denominacion FROM partidasIngresos WHERE partida = ?", (clave,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "No encontrada"

def llenar_denominacion(event, entrada_clave, entrada_resultado):
    clave = entrada_clave.get()
    denominacion = buscar_denominacion_db(clave)
    entrada_resultado.configure(state="normal")
    entrada_resultado.delete(0, tk.END)
    entrada_resultado.insert(0, denominacion)
    entrada_resultado.configure(state="readonly")
    
    

def agregar_fila_buscar():
    # añadir otra fila
    fila_Actual[0] += 1
    # nuevo entry 
    nueva_partida = ctk.CTkEntry(frame1, placeholder_text="Clave")
    nueva_partida.grid(row=fila_Actual[0], column=0, padx=10, pady=5)
    
    nuevo_resultado = ctk.CTkEntry(frame1, placeholder_text="Denominacion")
    nuevo_resultado.configure(state="readonly")
    nuevo_resultado.grid(row=fila_Actual[0], column=1, padx=10, pady=5)
    
    nuevo_abono = ctk.CTkEntry(frame1, placeholder_text="Abono")
    nuevo_abono.grid(row=fila_Actual[0], column=2, padx=10, pady=5)
    
    entradas.extend([nueva_partida, nuevo_resultado, nuevo_abono])
    
    nueva_partida.bind("<FocusOut>", lambda event: llenar_denominacion(event, nueva_partida, nuevo_resultado))
    
    # boton para recorrer el boton
    btnOK.grid(row=fila_Actual[0], column=3, padx=10, pady=10)
    
    nueva_partida.focus_set()  # Enfocar el nuevo entry


partida = ctk.CTkEntry(frame1, placeholder_text="Partida")
partida.grid(row=0, column=0, padx=10)
partida.focus()  # Enfocar el primer entry

resultado = ctk.CTkEntry(frame1, placeholder_text="Resultado")
resultado.configure(state="readonly")
resultado.grid(row=0, column=1, padx=10)

abono = ctk.CTkEntry(frame1, placeholder_text="Abono")
abono.grid(row=0, column=2, padx=10)

partida.bind("<FocusOut>", lambda event: llenar_denominacion(event, partida, resultado))

btnOK = ctk.CTkButton(frame1, text="SI", command=agregar_fila_buscar)
btnOK.grid(row=0, column=3, padx=10)


# --- BOTONES PARA GUARDAR Y PARA GENERAR EL ARCHIVO ---
frame2 = ctk.CTkFrame(app, fg_color="transparent")
frame2.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)
btnGuardar = ctk.CTkButton(frame2, text="Guardar")
btnGuardar.grid(row=0, column=0, padx=10)
btnGenerar = ctk.CTkButton(frame2, text="Descargar")
btnGenerar.grid(row=0, column=1, padx=10)


app.mainloop()
