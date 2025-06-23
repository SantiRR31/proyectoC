import tkinter as tk
import customtkinter as ctk
import sqlite3
from PIL import Image
from customtkinter import CTkImage
from utils.utils import convertir_a_mayusculas
from widgets.widgets import crear_boton_imagen
import xlwings as xw
import os
from tkcalendar import DateEntry
from tkinter import messagebox
from functions import genRegIngresos, funcions
from datetime import datetime
import psutil, time
from utils.config_utils import cargar_config
from utils.rutas import ruta_absoluta
import shutil

CONFIG_PATH = "config.json"

def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD-MM-AAAA'."""
    return datetime.datetime.now().strftime("%d-%m-%Y")

def mostrar_formulario_ingresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()
        
    config = cargar_config()
    # --- TÍTULO ---
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
    lbl_fecha = ctk.CTkLabel(entrada_frame, text="Fecha del voucher:", font=("Arial", 14))
    lbl_fecha.grid(row=0, column=0, padx=(10,5), pady=5, sticky="w")
    fecha_policia = DateEntry(entrada_frame, placeholder_text="📅 Fecha de ingreso", font=("Helvetica", 14), locale="es")
    fecha_policia.grid(row=0, column=1, padx=(5,10), pady=5, sticky="ew")
    #fecha_policia.insert(0, obtener_fecha_actual())
    #fecha_policia.configure(state="readonly")
    
    lbl_no_poliza = ctk.CTkLabel(entrada_frame, text="No. Póliza:", font=("Arial", 14))
    lbl_no_poliza.grid(row=0, column=2, padx=(10,5), pady=5, sticky="w")
    num_polizas = [str(i) for i in range(1, 32)]
    no_poliza = ctk.CTkOptionMenu(entrada_frame, values=num_polizas)
    no_poliza.set("No. Póliza")  # Texto inicial
    no_poliza.grid(row=0, column=3, padx=(5,10), pady=5, sticky="ew")

    # Fila 2 - Banco y Cargo o Importe
    lbl_banco = ctk.CTkLabel(entrada_frame, text="Banco/Caja:", font=("Arial", 14))
    lbl_banco.grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
    banco_o_caja = ctk.CTkEntry(entrada_frame, placeholder_text="🏦 Banco o Caja")
    banco_o_caja.grid(row=1, column=1, padx=(5,10), pady=5, sticky="ew")
    banco_o_caja.insert(0, config.get("banco_caja", "BANNORTE"))  # Cargar valor por defecto

    lbl_cuanto_pago = ctk.CTkLabel(entrada_frame, text="Cargo/Importe:", font=("Arial", 14))
    lbl_cuanto_pago.grid(row=1, column=2, padx=(10,5), pady=5, sticky="w")
    cuanto_pago = ctk.CTkEntry(entrada_frame, placeholder_text="Importe")
    cuanto_pago.grid(row=1, column=3, padx=(5,10), pady=5, sticky="ew")

    # Fila 3 - Notas adicionales de la póliza
    lbl_nota = ctk.CTkLabel(entrada_frame, text="Nota:", font=("Arial", 14))
    lbl_nota.grid(row=2, column=0, padx=(10,5), pady=5, sticky="w")
    nota = ctk.CTkEntry(entrada_frame, placeholder_text="Notas adicionales")
    nota.grid(row=2, column=1, columnspan=3, padx=(5,10), pady=5, sticky="ew")
    nota.bind("<KeyRelease>", lambda event: convertir_a_mayusculas(nota, event))
    
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
        origen_db = ruta_absoluta("prueba.db")
        destino_db = os.path.join(os.getcwd(), "prueba.db")
        
        # Si no existe ya en destino, copiarla
        if not os.path.exists(destino_db):
            try:
                shutil.copy(origen_db, destino_db)
            except Exception as e:
                print(f"Error al copiar la base de datos: {e}")
                return "Error al acceder DB"
        
        try:
            conn = sqlite3.connect('prueba.db')
            cursor = conn.cursor()
            cursor.execute("SELECT denominacion FROM partidasIngresos WHERE partida = ?", (clave,))
            resultado = cursor.fetchone()
            conn.close()
            return resultado[0] if resultado else "No encontrada"
        except Exception as e:
            print(f"Error al consultar la base de datos: {e}")
            return "Error en consulta"

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
                    #btn_guardar.configure(state="normal")
                    btn_descargar.configure(state="normal")
                else:
                    validacion_totales.configure(text="❌", text_color="#d10d2f")
                    #btn_guardar.configure(state="disabled")
                    btn_descargar.configure(state="disabled")
            else:
                validacion_totales.configure(text="❌", text_color="gray")
                #btn_guardar.configure(state="disabled")
                btn_descargar.configure(state="disabled")           
        except ValueError:
            pass  # Ignorar errores si algún campo tiene un valor no numérico
            #btn_guardar.configure(state="disabled")
            btn_descargar.configure(state="disabled")
            
    def eliminar_fila(fila, tupla):
        fila.destroy()
        entradas.remove(tupla)

    def agregar_fila(enfocar_nueva_clave=False):
        fila_frame = ctk.CTkFrame(frame_filas, fg_color="transparent", corner_radius=15)
        fila_frame.pack(fill="x", pady=5)

        entrada_clave = ctk.CTkEntry(fila_frame, placeholder_text="Clave")
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
        app = None
        wb = None
        try:
            # Obtener valores de la interfaz
            banco = banco_o_caja.get()
            cargo_importe = cuanto_pago.get()
            notaAdicional = nota.get()
            noPoliza = no_poliza.get()
    
            # Manejo de fechas
            fecha_ingresada = fecha_policia.get_date()
            fecha1 = fecha_ingresada.day
            fecha2 = fecha_ingresada.month
            fecha3 = fecha_ingresada.year
    
            # Obtener mes/año actual
            fech_act = datetime.now()
            mes = fech_act.strftime('%b').lower()
            anio = fech_act.year
            poliza_final = f"{noPoliza}/{mes}/{anio}"
        
            # Configurar rutas PRIMERO (antes de abrir Excel)
            carpetaBase = r"C:\Cecati122"
            carpeta_descargas = os.path.join(carpetaBase, "PolizasDeIngresos")
            os.makedirs(carpeta_descargas, exist_ok=True)
            nombre_archivo = f"Poliza_ingresos_{mes}_{anio}.xlsx"
            ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)
        
            app = xw.App(visible=False)  # Iniciar Excel primero
        
            retries = 0
            max_retries = 3
            while retries < max_retries:
                try:
                    if os.path.exists(ruta_completa):
                        wb = app.books.open(ruta_completa)
                    else:
                        wb = app.books.open(ruta_absoluta("assets/plantillaIngresos.xlsx"))

                    break
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        # Limpiar procesos de Excel antes de reintentar
                        for proc in psutil.process_iter():
                            if "EXCEL.EXE" in proc.name().upper():
                                proc.kill()
                        time.sleep(1)
                        if os.path.exists(ruta_completa):
                            wb = app.books.open(ruta_completa)
                        else:
                            wb = app.books.open(ruta_absoluta("assets/plantillaIngresos.xlsx"))
                        break
                    time.sleep(2)  # Esperar 2 segundos antes de reintentar
    
            # Identificar plantilla
            if os.path.exists(ruta_completa):
                plantilla = wb.sheets["Plantilla Ingresos"]
            else:
                plantilla = wb.sheets["Plantilla Ingresos"]
                # Crear copia temporal
                hoja_temp = plantilla.copy(after=plantilla)
                hoja_temp.name = "Temp"
                plantilla.visible = False
    
            # ►►► GENERAR NOMBRE DE HOJA SEGURO ◄◄◄
            base_name = f"Pz {noPoliza}"[:20]
            timestamp_suffix = datetime.now().strftime('%H%M')
            existing_names = [s.name for s in wb.sheets]
        
            if any(name.startswith(base_name) for name in existing_names):
                nombre_hoja = f"{base_name}_{timestamp_suffix}"[:31]
            else:
                nombre_hoja = base_name[:31]
        
            if os.path.exists(ruta_completa):
                nueva_hoja = plantilla.copy(after=plantilla)
            else:
                nueva_hoja = wb.sheets["Temp"]
        
            nueva_hoja.name = nombre_hoja
            nueva_hoja.visible = True  # Asegurar visibilidad
            nueva_hoja.activate()      # Activar la hoja
            hoja_activa = nueva_hoja
    
            # ESCRITURA DE DATOS
            hoja_activa.range("A10").value = banco
            hoja_activa.range("AS10").value = float(cargo_importe)
            hoja_activa.range("J40").value = notaAdicional
            hoja_activa.range("AT6").value = poliza_final
            hoja_activa.range("AL6").value = fecha1
            hoja_activa.range("AN6").value = fecha2
            hoja_activa.range("AQ6").value = fecha3
    
            suma_por_clave = {}
            
            # ENTRADAS DINÁMICAS
            for entrada_clave, _, entrada_abono in entradas:
                clave = entrada_clave.get()
                abono = entrada_abono.get()
                
                if clave:
                    try:
                        abono_val = float(abono)
                    except (ValueError, TypeError):
                        abono_val = 0.0
                    
                    if clave in suma_por_clave:
                        suma_por_clave[clave] += abono_val
                    else:
                        suma_por_clave[clave] = abono_val
                
            fila_inicial = 15
            for clave, total_abono in suma_por_clave.items():
                hoja_activa.range(f"B{fila_inicial}").value = clave
                hoja_activa.range(f"AT{fila_inicial}").value = total_abono
                fila_inicial += 1
    
            # GUARDADO Y CIERRE SEGURO
            wb.save(ruta_completa)
            wb.close()
            app.quit()
        
            success_msg = (
                "Póliza guardada exitosamente!\n"
                f"Archivo: {nombre_archivo}\n"
                f"Ubicación: {carpeta_descargas}\n"
                f"Hoja creada: {nombre_hoja}\n\n"
                f"N° Póliza: {noPoliza} | Importe: ${cargo_importe}"
            )
            messagebox.showinfo("Operación Exitosa", success_msg)

        except Exception as e:
            error_type = type(e).__name__
            error_msg = (
                f"Error ({error_type}): {str(e)}\n\n"
                "Posibles soluciones:\n"
                "1. Cierre todas las instancias de Excel\n"
                "2. Verifique permisos de escritura en:\n"
                f"   > {carpeta_descargas}\n"
                "3. Revise que los datos tengan formato válido\n"
                "4. Confirme que la plantilla exista en:\n"
                "   > assets/plantillaIngresos.xlsx"
            )
            messagebox.showerror("Error Crítico", error_msg)
        
        finally:
            try:
                if wb is not None:
                    wb.close()
            except:
                pass
        
            try:
                if app is not None:
                    app.quit()
                    app.kill()
            except:
                pass
        
            # Limpieza adicional de procesos
            for proc in psutil.process_iter():
                try:
                    if "EXCEL.EXE" in proc.name().upper():
                        try:
                            proc.kill()
                        except:
                            pass
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            
    def guardar_datos_en_db():
        try:
            conn = sqlite3.connect('prueba.db')
            cursor = conn.cursor()

            # --- Guardar datos en polizasIngresos ---
            fecha_cruda = fecha_policia.get().strip()
            try:
                fecha = datetime.strptime(fecha_cruda, '%d/%m/%y').strftime('%d/%m/%Y')
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido.")
                return
            #fecha = fecha_policia.get().strip()
            
            no = no_poliza.get().strip()
            banco = banco_o_caja.get().strip()
            importe = cuanto_pago.get().strip()
            nota_texto = nota.get().strip()

            if not (fecha and no and banco and importe):
                messagebox.showerror("Error", "Por favor completa todos los campos obligatorios.")
                return

            cursor.execute("""
                INSERT OR REPLACE INTO polizasIngresos (fecha, noPoliza, banco, importe, nota)
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

    # si queremos fucionar los votones de guardar y de descargar
    def guardar_descargar():
        try:
            guardar_datos_en_db()
            guardar_Ingresos()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrio un error: {e}")

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

    imgGenerarReporte = Image.open(ruta_absoluta("assets/generate.png"))
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
    
    imgVerDescargas = Image.open(ruta_absoluta("assets/look.png"))
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
    
    #imgBtnGuardar = Image.open(ruta_absoluta("assets/check.png"))
    #btn_guardar = ctk.CTkButton(
    #    botones_frame, 
    #    text="Guardar", 
    #    width=120, 
    #    fg_color="#004b8f", 
    #    hover_color="#0065a5", 
    #    corner_radius=32,
    #    image=CTkImage(imgBtnGuardar, size=(20, 20)),  # nota: es "image", no "Image"
    #    command=guardar_datos_en_db
    #)
    #btn_guardar.pack(side="right", padx=10)

    imgBtnDescargar = Image.open(ruta_absoluta("assets/downlo.png"))
    btn_descargar = ctk.CTkButton(
        botones_frame,
        text="Guardar y Descargar",
        width=120,
        fg_color="#008d62",
        hover_color="#2ca880",
        corner_radius=32,
        image=CTkImage(imgBtnDescargar, size=(20, 20)), # nota: es "image", no "Image",
        command=guardar_descargar
    )
    btn_descargar.pack(side="right", padx=10)
