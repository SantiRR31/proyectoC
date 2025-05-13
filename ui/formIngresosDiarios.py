import tkinter as tk
import customtkinter as ctk
import os

def mostar_formulario_ingreos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()
        widget.destroy()
   
    # --- INTERFAZ PRINCIPAL ---
    tittle = ctk.CTkLabel(frame_padre, text="Control de ingresos diarios", font=("Arial", 24))
    tittle.pack(pady=20)

    frame1 = ctk.CTkFrame(frame_padre, fg_color="transparent")
    frame1.pack(pady=20)

    fila_Actual = [0]
    entradas = []

    def agregar_fila():
        fila_Actual[0] += 1
        nueva_partida = ctk.CTkEntry(frame1, placeholder_text="Partida")
        nueva_partida.grid(row=fila_Actual[0], column=0, padx=10, pady=5)
        nuevo_resultado = ctk.CTkEntry(frame1, placeholder_text="Resultado")
        nuevo_resultado.grid(row=fila_Actual[0], column=1, padx=10, pady=5)
        entradas.append(nueva_partida)
        entradas.append(nuevo_resultado)
        btnOK.grid(row=fila_Actual[0], column=2, padx=10, pady=10)

    partida = ctk.CTkEntry(frame1, placeholder_text="Partida")
    partida.grid(row=0, column=0, padx=10)
    resultado = ctk.CTkEntry(frame1, placeholder_text="Resultado")
    resultado.grid(row=0, column=1, padx=10)
    btnOK = ctk.CTkButton(frame1, text="SI", command=agregar_fila)
    btnOK.grid(row=0, column=2, padx=10)

    # Botones guardar y descargar
    frame2 = ctk.CTkFrame(frame_padre, fg_color="transparent")
    frame2.place(relx=1.0, rely=1.0, anchor="se", x=-40, y=-40)

    btnGuardar = ctk.CTkButton(frame2, text="Guardar")
    btnGuardar.grid(row=0, column=0, padx=10)

    btnGenerar = ctk.CTkButton(frame2, text="Descargar")
    btnGenerar.grid(row=0, column=1, padx=10)

    btnRegresar = ctk.CTkButton(frame2, text="Regresar al menú")
    btnRegresar.grid(row=0, column=2, padx=10)



