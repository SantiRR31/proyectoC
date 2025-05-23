import tkinter as tk
import customtkinter as ctk
import sqlite3
import datetime
from PIL import Image
from customtkinter import CTkImage
from widgets.widgets import crear_boton_imagen
import xlwings as xw
import os
from tkinter import messagebox
from functions import genRegIngresos, funcions
from tkcalendar import DateEntry



from styles.styles import (
    FUENTE_FORMULARIO_T,
    FUENTE_FORMULARIO_S,
    FONDO_CONTENEDORES,
    ENTRADA_FRAME_C,
    FUENTE_LABEL,
    FUENTE_SECCION_TITULO,
    FUENTE_VALIDACION,
    btn_eliminar_style,
    btn_agregar_style,
    btn_guardar_style,
    btn_descargar_style,
    COLOR_VALIDACION_OK,
    COLOR_VALIDACION_ERROR,
    COLOR_VALIDACION_NEUTRO,
)


def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD-MM-AAAA'."""
    return datetime.datetime.now().strftime("%d-%m-%Y")

def mostrar_formulario_ingresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    titulo = ctk.CTkLabel(frame_padre, text="Póliza de Ingresos", font=("Arial", 28, "bold"))
    titulo.pack(pady=30)

    # --- CONTENEDOR PRINCIPAL (Scroll + Botones fijos) ---
    contenedor_principal = ctk.CTkFrame(frame_padre, fg_color="transparent" , corner_radius=15)
    contenedor_principal.pack(fill="both", expand=True)

    # --- CONTENIDO CON SCROLL ---
    contenedor_general = ctk.CTkScrollableFrame(contenedor_principal, fg_color="transparent", corner_radius=15)
    contenedor_general.pack(fill="both", expand=True, padx=30, pady=(10, 0))  # sin padding abajo

    for i in range(3):
        contenedor_general.grid_columnconfigure(i, weight=1)

    # --- SECCIÓN DATOS PÓLIZA ---
    seccion_poliza = ctk.CTkFrame(contenedor_general, fg_color="transparent", corner_radius=15)
    seccion_poliza.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 20))

    label_poliza = ctk.CTkLabel(seccion_poliza, text="Datos de la Póliza", font=("Arial", 20, "bold"))
    label_poliza.pack(anchor="w", pady=10)

    entrada_frame = ctk.CTkFrame(seccion_poliza, fg_color="transparent", corner_radius=15)
    entrada_frame.pack(fill="x")
    
    # Configuración de columnas para labels + entries
    entrada_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
    
    # Fila 1 - Fecha y Número de Póliza
    lbl_fecha = ctk.CTkLabel(entrada_frame, text="Fecha:", font=("Arial", 14))
    lbl_fecha.grid(row=0, column=0, padx=(10,5), pady=5, sticky="w")
    fecha_policia = DateEntry(entrada_frame, placeholder_text="📅 Fecha de ingreso")
    fecha_policia.grid(row=0, column=1, padx=(5,10), pady=5, sticky="ew")
    #fecha_policia.insert(0, obtener_fecha_actual())
    #fecha_policia.configure(state="readonly")
    
    lbl_no_poliza = ctk.CTkLabel(entrada_frame, text="No. Póliza:", font=("Arial", 14))
    lbl_no_poliza.grid(row=0, column=2, padx=(10,5), pady=5, sticky="w")
    num_polizas = [str(i) for i in range(1, 101)]
    no_poliza = ctk.CTkOptionMenu(entrada_frame, values=num_polizas)
    no_poliza.set("🔢 No. Póliza")  # Texto inicial
    no_poliza.grid(row=0, column=3, padx=(5,10), pady=5, sticky="ew")

    # Fila 2 - Banco y Cargo o Importe
    lbl_banco = ctk.CTkLabel(entrada_frame, text="Banco/Caja:", font=("Arial", 14))
    lbl_banco.grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
    banco_o_caja = ctk.CTkEntry(entrada_frame, placeholder_text="🏦 Banco o Caja")
    banco_o_caja.grid(row=1, column=1, padx=(5,10), pady=5, sticky="ew")

    lbl_cuanto_pago = ctk.CTkLabel(entrada_frame, text="Cargo/Importe:", font=("Arial", 14))
    lbl_cuanto_pago.grid(row=1, column=2, padx=(10,5), pady=5, sticky="w")
    cuanto_pago = ctk.CTkEntry(entrada_frame, placeholder_text="💰 Importe")
    cuanto_pago.grid(row=1, column=3, padx=(5,10), pady=5, sticky="ew")

    # Fila 3 - Notas adicionales de la póliza
    lbl_nota = ctk.CTkLabel(entrada_frame, text="Nota:", font=("Arial", 14))
    lbl_nota.grid(row=2, column=0, padx=(10,5), pady=5, sticky="w")
    nota = ctk.CTkEntry(entrada_frame, placeholder_text="📝 Notas adicionales")
    nota.grid(row=2, column=1, columnspan=3, padx=(5,10), pady=5, sticky="ew")

    entrada_frame.grid_columnconfigure((0, 1), weight=1)

    # --- SECCIÓN FILAS ADICIONALES ---
    seccion_filas = ctk.CTkFrame(contenedor_general, fg_color="transparent", corner_radius=15)
    seccion_filas.grid(row=2, column=0, columnspan=3, sticky="ew")

    label_filas = ctk.CTkLabel(seccion_filas, text="Clave", font=("Arial", 20, "bold"))
    label_filas.pack(anchor="w", pady=10)

    frame_filas = ctk.CTkFrame(seccion_filas, fg_color="transparent", corner_radius=15)
    frame_filas.pack(fill="x")

    entradas = []

    def buscar_denominacion_db(clave):
        conn = sqlite3.connect('prueba.db')
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
        
    # Funcion para ir sumando los valores de la entrada de abono e ir actualizando el total
    def actualizar_total():
        """Suma los valores de los campos de abono y actualiza el campo total."""
        try:
            suma_total = sum(float(entrada[2].get()) for entrada in entradas if entrada[2].get().strip())
            total.configure(state="normal")
            total.delete(0, tk.END)
            total.insert(0, f"{suma_total:.2f}")
            total.configure(state="readonly")
            
            #validar si el total es igual al importe
            importe_valor = cuanto_pago.get().strip()
            if importe_valor:
                importe_float = float(importe_valor)
                if abs(importe_float - suma_total) < 0.01:
                    validacion_totales.configure(text="✅", text_color="#008d62")
                    btn_guardar.configure(state="normal")
                    btn_descargar.configure(state="normal")
                else:
                    validacion_totales.configure(text="❌", text_color="#d10d2f")
                    btn_guardar.configure(state="disabled")
                    btn_descargar.configure(state="disabled")
            else:
                validacion_totales.configure(text="❌", text_color="gray")
                btn_guardar.configure(state="disabled")
                btn_descargar.configure(state="disabled")           
        except ValueError:
            pass  # Ignorar errores si algún campo tiene un valor no numérico
            btn_guardar.configure(state="disabled")
            btn_descargar.configure(state="disabled")
            
    def eliminar_fila(fila, tupla):
        fila.destroy()
        entradas.remove(tupla)

    def agregar_fila(enfocar_nueva_clave=False):
        fila_frame = ctk.CTkFrame(frame_filas, fg_color="transparent", corner_radius=15)
        fila_frame.pack(fill="x", pady=5)

        entrada_clave = ctk.CTkEntry(fila_frame, placeholder_text="🔑 Clave")
        entrada_clave.grid(row=0, column=0, padx=10, sticky="ew")

        entrada_resultado = ctk.CTkEntry(fila_frame, placeholder_text="Denominación", state="disabled")
        entrada_resultado.grid(row=0, column=1, padx=10, sticky="ew")

        entrada_abono = ctk.CTkEntry(fila_frame, placeholder_text="Abono")
        entrada_abono.grid(row=0, column=2, padx=10, sticky="ew")
        entrada_abono.bind("<KeyRelease>", lambda event: actualizar_total())


        entrada_clave.bind("<FocusOut>", lambda event: llenar_denominacion(event, entrada_clave, entrada_resultado))
        entrada_clave.bind("<Return>", lambda event: entrada_abono.focus_set())
        entrada_abono.bind("<Return>", lambda event: agregar_fila(enfocar_nueva_clave=True))

        tupla = (entrada_clave, entrada_resultado, entrada_abono)
        btn_eliminar = ctk.CTkButton(
            fila_frame,
            text="❌",
            width=30, 
            fg_color="#d10d2f", 
            hover_color="#d93954", 
            corner_radius=5,
            command=lambda f=fila_frame, t=tupla: eliminar_fila(f, t)
        )
        btn_eliminar.grid(row=0, column=3, padx=5)
        entradas.append(tupla)

        fila_frame.grid_columnconfigure((0, 1, 2), weight=1)

        if enfocar_nueva_clave:
            entrada_clave.focus_set()

    agregar_fila()
    

    def guardar_Ingresos():
        try:
            # Abrimos Excel de forma controlada
            app = xw.App(visible=False)
            wb = app.books.open("assets/plantillaIngresos.xlsx")
            hoja = wb.sheets["Plantilla Ingresos"]

            # Tomamos los valores de los Entry
            banco = banco_o_caja.get()
            cargo_importe = cuanto_pago.get()
            notaAdicional = nota.get()
            noPoliza = no_poliza.get()
            fecha_ingresada = fecha_policia.get_date()
            fecha1 = fecha_ingresada.strftime("%d")
            fecha2 = fecha_ingresada.strftime("%m") 
            fecha3 = fecha_ingresada.strftime("%y")

            hoja.range("A10").value = banco
            hoja.range("AS10").value = cargo_importe
            hoja.range("J40").value = notaAdicional
            hoja.range("AT6").value = noPoliza
            hoja.range("AL6").value = fecha1
            hoja.range("AN6").value = fecha2
            hoja.range("AQ6").value = fecha3
            
            # Entradas dinámicas
            fila_inicial = 15
            for entrada_clave, _, entrada_abono in entradas:
                clave = entrada_clave.get()
                abono = entrada_abono.get()
                hoja.range(f"B{fila_inicial}").value = clave
                hoja.range(f"AT{fila_inicial}").value = float(abono) if abono else 0.0
                fila_inicial += 1

            # Crear carpeta de destino
            fecha_hoy = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre_archivo = f"Poliza_ingresos_{no_poliza.get()}.xlsx"
            carpetaBase = r"C:\Cecati122"
            carpeta_descargas = os.path.join(carpetaBase, "PolizasDeIngresos")
            os.makedirs(carpeta_descargas, exist_ok=True)
            ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)

            # Guardamos el archivo
            wb.save(ruta_completa)
            messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_completa}")

            # Cerrar libro y Excel
            wb.close()
            app.quit()

        except Exception as e:
            messagebox.showerror("Error al guardar", f"Ocurrió un error:\n{e}")
            
    def guardar_datos_en_db():
        try:
            conn = sqlite3.connect('prueba.db')
            cursor = conn.cursor()

            # --- Guardar datos en polizasIngresos ---
            fecha = fecha_policia.get().strip()
            no = no_poliza.get().strip()
            banco = banco_o_caja.get().strip()
            importe = cuanto_pago.get().strip()
            nota_texto = nota.get().strip()

            if not (fecha and no and banco and importe):
                messagebox.showerror("Error", "Por favor completa todos los campos obligatorios.")
                return

            cursor.execute("""
                INSERT INTO polizasIngresos (fecha, noPoliza, banco, importe, nota)
                VALUES (?, ?, ?, ?, ?)
            """, (fecha, no, banco, float(importe), nota_texto))

            # --- Guardar entradas en detallePolizaIngreso ---
            for clave_entry, _, abono_entry in entradas:
                clave = clave_entry.get().strip()
                abono = abono_entry.get().strip()
                if clave and abono:
                    cursor.execute("""
                        INSERT INTO detallePolizaIngreso (noPoliza, clave, abono)
                        VALUES (?, ?, ?)
                    """, (no, clave, float(abono)))

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        
        except Exception as e:
            messagebox.showerror("Error al guardar", f"Ocurrió un error: {e}")

    

    btn_agregar_fila = ctk.CTkButton(seccion_filas, text="➕ Agregar", command=agregar_fila, corner_radius=32,
                                     fg_color="#008d62", hover_color="#2ca880")
    btn_agregar_fila.pack(pady=10)

    # --- BOTONES FINALES FIJOS ABAJO ---
    botones_frame = ctk.CTkFrame(contenedor_principal, fg_color="transparent", corner_radius=15)
    botones_frame.pack(fill="x", pady=10, padx=20, anchor="e")
    
    llb_total = ctk.CTkLabel(botones_frame, text="Total:", font=("Arial", 16))
    llb_total.pack(side="left", padx=(0, 10))
    total = ctk.CTkEntry(botones_frame, placeholder_text="💰 Total", state="readonly")
    total.pack(side="left", padx=(0, 10), fill="x", expand=False)
    
    validacion_totales = ctk.CTkLabel(botones_frame, text="❌", font=("Arial", 20))
    validacion_totales.pack(side="left", padx=(0, 10))
    
    
    """ crear_boton_imagen(botones_frame,"Ver Descargas", "assets/look.png",btn_guardar_style,abrir_carpeta,side ="right",padx= 10)    
    btn_guardar = crear_boton_imagen(botones_frame, "Guardar", "assets/check.png", btn_guardar_style, None, side="right", padx=10)
    btn_descargar = crear_boton_imagen(botones_frame, "Descargar", "assets/downlo.png", btn_descargar_style, None, side="right", padx=10) """

    imgGenerarReporte = Image.open("assets/generate.png")
    btn_generar_reporte = ctk.CTkButton(
        botones_frame,
        text="Generar Reporte Mensual",
        width=120,
        fg_color="#004b8f", 
        hover_color="#0065a5", 
        corner_radius=32,
        image=CTkImage(imgGenerarReporte, size=(20, 20)),
        command=genRegIngresos.confirmar_y_generar
    )
    btn_generar_reporte.pack(side="right", padx=10)
    
    imgVerDescargas = Image.open("assets/look.png")
    btn_ver_descargas = ctk.CTkButton(
        botones_frame,
        text="Ver Descargas",
        width=120,
        fg_color="#004b8f", 
        hover_color="#0065a5", 
        corner_radius=32,
        image=CTkImage(imgVerDescargas, size=(20, 20)),
        command=lambda: funcions.abrir_carpeta()
    )
    btn_ver_descargas.pack(side="right", padx=10)
    
    imgBtnGuardar = Image.open("assets/check.png")
    btn_guardar = ctk.CTkButton(
        botones_frame, 
        text="Guardar", 
        width=120, 
        fg_color="#004b8f", 
        hover_color="#0065a5", 
        corner_radius=32,
        image=CTkImage(imgBtnGuardar, size=(20, 20)),  # nota: es "image", no "Image"
        command=guardar_datos_en_db
    )
    btn_guardar.pack(side="right", padx=10)

    imgBtnDescargar = Image.open("assets/downlo.png")
    btn_descargar = ctk.CTkButton(
        botones_frame,
        text="Descargar",
        width=120,
        fg_color="#008d62",
        hover_color="#2ca880",
        corner_radius=32,
        image=CTkImage(imgBtnDescargar, size=(20, 20)), # nota: es "image", no "Image",
        command=guardar_Ingresos
    )
    btn_descargar.pack(side="right", padx=10)
