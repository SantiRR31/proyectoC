import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from widgets.widgets import *
from styles.styles import *
from utils.config_utils import cargar_config
import sqlite3
import xlwings as xw
import os
from datetime import datetime
from tkinter import messagebox
from functions.genRegIngresos import generar_reporte_xlwings

def mostrar_detalles_ingresos(frame_padre):
    #if not hasattr(mostrar_detalles_ingresos, "refresco"):
    
    for widget in frame_padre.winfo_children():
        widget.destroy()

    config = cargar_config()

    ctk.CTkLabel(frame_padre, text="Detalles de ingresos", font=FUENTE_FORMULARIO_T).pack(pady=30)
    
    # Contenedor para la tabla
    contenedor_tabla = ctk.CTkFrame(frame_padre)
    contenedor_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    ## Frame contenedor para Treeview y scrollbar - usar tk.Frame con fondo oscuro manual
    modo = ctk.get_appearance_mode()
    if modo == "Dark":
        color_fondo = "#1e1e1e"
    else:
        color_fondo = "white"

    frame_tree = tk.Frame(contenedor_tabla, bg=color_fondo)  # Aquí sí se puede usar bg
    frame_tree.pack(fill="both", expand=True)
    
    columnas = ("fecha", "Poliza", "banco", "importe", "nota")
    estilo_tabla()
    
    estilo_act = "Dark.Treeview" if modo == "Dark" else "Light.Treeview"
    tabla = ttk.Treeview(frame_tree, columns=columnas, show="headings", style=estilo_act)
    
    anchos = {
        "fecha": 135,     # Fecha (dd/mm/yyyy)
        "Poliza": 135,    # Número de póliza
        "banco": 200,     # Nombre del banco
        "importe": 150,   # Valor numérico
        "nota": 200       # Notas (más ancho por texto variable)
    }

    # Manejar color de fondo del widget según modo
    if modo == "Dark":
        tabla.tk_setPalette(background="#1e1e1e")
    else:
        tabla.tk_setPalette(background="white")
    
    for col in columnas:
        # Configurar cabecera
        tabla.heading(col, text=col.capitalize())
    
        # Configurar propiedades de columna
        tabla.column(
            col, 
            anchor="center" if col in ["fecha", "Poliza", "banco"] else "e" if col == "importe" else "w",              # Alineación (w=izquierda)
            width=anchos[col],       # Ancho personalizado
            minwidth=100,             # Ancho mínimo al redimensionar
            stretch=True if col == "nota" else False  # Solo "nota" se expande
        )
        
    tabla.update_idletasks()  # Actualiza cálculos de layout
    contenedor_tabla.update()  # Asegura que el contenedor padre se actualice
    
    tabla.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tabla.yview)
    scrollbar.pack(side="right", fill="y")

    tabla.configure(yscrollcommand=scrollbar.set)

    # Conectar a la base de datos
    conexion = sqlite3.connect("prueba.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, fecha, noPoliza, banco, importe, nota FROM polizasIngresos ORDER BY STRFTIME('%Y-%m-%d', SUBSTR(fecha, 7, 4) || '-' || SUBSTR(fecha, 4, 2) || '-' || SUBSTR(fecha, 1, 2)) DESC")
    registros = cursor.fetchall()
    
    conexion.close()

    if not registros:
        ctk.CTkLabel(contenedor_tabla, text="No hay registros.", font=("Arial", 14)).pack(pady=20)
        return

    # Insertar registros
    for fila in registros:
        id_registro = fila[0]
        fecha, poliza, banco, importe, nota = fila[1:]
        importe_formateado = f"${importe:,.2f}"
        
        valores_visibles = (fecha, poliza, banco, importe_formateado, nota)
        tabla.insert("", "end", values=valores_visibles, iid=id_registro)

    # Botones para editar y eliminar seleccionados
    frame_botones = ctk.CTkFrame(frame_padre, fg_color="transparent")
    frame_botones.pack(fill="x", pady=10)

    frame_centro = ctk.CTkFrame(frame_botones, fg_color="transparent")
    frame_centro.pack(side="left", expand=True)
    
    frame_derecha = ctk.CTkFrame(frame_botones, fg_color="transparent")
    frame_derecha.pack(side="right")

    def obtener_seleccion():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "¡Selecciona un registro!")
            return None
        valores = tabla.item(seleccionado)["values"]
        id_registro = seleccionado
        return [id_registro] + valores

    btn_editar = ctk.CTkButton(frame_centro, text="Editar seleccionado", text_color="black", fg_color="#ffd300", hover_color="#ffb201", command=lambda: (
        (datos := obtener_seleccion()) and editar_registro(*datos, frame_padre)
    ))
    btn_editar.pack(side="left", padx=10)

    btn_eliminar = ctk.CTkButton(frame_centro, text="Eliminar seleccionado", fg_color="#d10d2f", hover_color="#d93954",
        command=lambda: (
            (datos := obtener_seleccion()) and eliminar_registro(datos[0], frame_padre)
    ))
    btn_eliminar.pack(side="left", padx=10)
    
    btn_generar = ctk.CTkButton(frame_derecha, text="Generar de nuevo", text_color="white", fg_color="#ff6961", hover_color="#c63637", border_color="#ff6961", border_width=2,command=confirmar_generar_reporte)
    btn_generar.pack(padx=10)

    # Eliminar registro
def eliminar_registro(id_registro, frame_padre):
    confirm = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?")
    if confirm:
        conexion = sqlite3.connect("prueba.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT fecha, noPoliza FROM polizasIngresos WHERE id = ?", (id_registro,))
        resultado = cursor.fetchone()
        if resultado:
            fecha, noPoliza = resultado
            cursor.execute("DELETE FROM polizasIngresos WHERE id = ?", (id_registro,))
            cursor.execute("DELETE FROM detallePolizaIngreso WHERE noPoliza = ? AND fecha = ?", (noPoliza, fecha))
        else:
            messagebox.showerror("Error", "El registro no se encontró")
        conexion.commit()
        conexion.close()
        
        try:
            fecha_obj = datetime.strptime(fecha,"%d/%m/%Y")
            mes = fecha_obj.strftime('%b').replace('.', '').lower()
            anio = fecha_obj.year
            
            nombre_archivo = f"Poliza_ingresos_{mes}_{anio}.xlsx"
            ruta_excel = os.path.join("C:\\Cecati122\\PolizasDeIngresos", nombre_archivo)
            
            if not os.path.exists(ruta_excel):
                    messagebox.showwarning("Advertencia", f"No se encontró el archivo Excel: {ruta_excel}")
                    return
                
            app = xw.App(visible=False)
            wb = app.books.open(ruta_excel)               
            
            # Buscar hoja que comience con "Pz {noPoliza}"
            hojas_a_eliminar = [
                hoja for hoja in wb.sheets if hoja.name.startswith(f"Pz {noPoliza}")
            ]
        
            if hojas_a_eliminar:
                for hoja in hojas_a_eliminar:
                    hoja.delete()
                wb.save()
                messagebox.showinfo("Éxito", f"Registro eliminado y hoja(s) '{noPoliza}' eliminadas del Excel.")
            else:
                messagebox.showwarning("Advertencia", f"No se encontró hoja para la póliza '{noPoliza}'.")
        
            wb.close()
            app.quit()
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al modificar el Excel:\n{e}")
            
    else:
        messagebox.showerror("Error", "El registro no se encontró.")    
        
        
    mostrar_detalles_ingresos(frame_padre)  # Refrescar vista
        
def editar_registro(id_registro, fecha_antigua, no_poliza_ant, banco_ant, importe_ant, nota_ant, frame_padre):
    ventana_editar = ctk.CTkToplevel()
    ventana_editar.title("Editar Registro")
    ventana_editar.geometry("500x700")
    
    # 🔁 SCROLLABLE FRAME GENERAL
    frame_scroll_general = ctk.CTkScrollableFrame(ventana_editar, width=480, height=680)
    frame_scroll_general.pack(padx=10, pady=10, fill="both", expand=True)

    entradas = {}
    campos = {
        "Fecha (dd/mm/yyyy)": fecha_antigua,
        "No. Póliza": no_poliza_ant,
        "Banco": banco_ant,
        "Importe": str(importe_ant),
        "Nota": nota_ant,
    }

    for campo, valor in campos.items():
        ctk.CTkLabel(frame_scroll_general, text=campo + ":").pack(pady=(20, 0))
        
        if campo == "Nota":
            entrada = ctk.CTkTextbox(frame_scroll_general, height=100)
            entrada.insert("1.0", valor)
        else:
            entrada = ctk.CTkEntry(frame_scroll_general)
            entrada.insert(0, valor)
        
        entrada.pack(fill="x", padx=20)
        entradas[campo] = entrada
        
    entrada_importe = entradas["Importe"]
    entrada_importe.bind("<KeyRelease>", lambda event: actualizar_validacion())

    # 🔁 FRAME DE ABONOS CON SCROLL (dentro del frame general)
    frame_abonos = ctk.CTkFrame(frame_scroll_general)
    frame_abonos.pack(fill="x", padx=20, pady=(30, 10))
    
    ctk.CTkLabel(frame_abonos, text="Abonos encontrados:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

    ctk.CTkLabel(frame_abonos, text="Clave", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(frame_abonos, text="Abono", font=ctk.CTkFont(weight="bold")).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
    entradas_detalles = []

    conn = sqlite3.connect("prueba.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, clave, abono
        FROM detallePolizaIngreso
        WHERE noPoliza = ? AND fecha = ?
    """, (no_poliza_ant, fecha_antigua))
    detalles = cursor.fetchall()

    if detalles:
        for i, (id, clave, abono) in enumerate(detalles, start=2):
            entrada_clave = ctk.CTkEntry(frame_abonos)
            entrada_clave.insert(0, clave)
            entrada_clave.grid(row=i, column=0, padx=10, pady=5)

            entrada_abono = ctk.CTkEntry(frame_abonos)
            entrada_abono.insert(0, str(abono))
            entrada_abono.grid(row=i, column=1, padx=10, pady=5)

            entrada_abono.bind("<KeyRelease>", lambda event: actualizar_validacion())

            entradas_detalles.append({
                "id": id,
                "clave": entrada_clave,
                "abono": entrada_abono
            })
    else:
        ctk.CTkLabel(
            frame_abonos,
            text="(No se encontraron abonos relacionados.)",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray"
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    
    label_suma = ctk.CTkLabel(frame_scroll_general, text="Suma de abonos: $0.00")
    label_suma.pack(pady=(20, 0))
    
    label_validacion = ctk.CTkLabel(frame_scroll_general, text="")
    label_validacion.pack(pady=(0, 10))

    def actualizar_validacion():
        suma = 0.0
        for detalle in entradas_detalles:
            abono_str = detalle["abono"].get().strip()
            try:
                abono = float(abono_str)
                suma += abono
            except:
                continue
            
        label_suma.configure(text=f"Suma de abonos: ${suma:.2f}")
        
        try:
            importe = float(entradas["Importe"].get().replace("$", "").replace(",", "").strip())
            if round(suma, 2) == round(importe, 2):
                label_validacion.configure(text="La suma de los abonos coincide con el importe", text_color="green")
            else:
                label_validacion.configure(text="La suma de los abonos NO coincide con el importe", text_color="red")
        except:
            label_validacion.configure(text="Importe no válido", text_color="orange")
    
    actualizar_validacion()

    def guardar():
        nueva_fecha = entradas["Fecha (dd/mm/yyyy)"].get()
        nuevo_poliza = entradas["No. Póliza"].get()
        nuevo_banco = entradas["Banco"].get()
        nuevo_importe = entradas["Importe"].get().replace("$", "").replace(",", "").strip()
        nueva_nota = entradas["Nota"].get("1.0", "end").strip()
        
        suma_abonos = 0.0
        for detalle in entradas_detalles:
            abono_text = detalle["abono"].get().strip()
            if not abono_text:
                continue
            try:
                abono_valor = float(abono_text)
            except ValueError:
                messagebox.showerror("Error", f"El abono '{abono_text}' no es un número válido")
                return
            suma_abonos += abono_valor
        
        try:
            importe_float = float(nuevo_importe)
        except ValueError:
            messagebox.showerror("Error", f"El importe ingresado no es valido.")
            return
        
        if round(suma_abonos, 2) != round(importe_float, 2):
            messagebox.showwarning(
                "Advertencia",
                f"La suma de los abonos ({suma_abonos:.2f}) no coincide con el importe total ({importe_float:.2f})."
            )
            return
        
        conexion = sqlite3.connect("prueba.db")
        cursor = conexion.cursor()
        
        cursor.execute("SELECT fecha, noPoliza FROM polizasIngresos WHERE id = ?", (id_registro,))
        resultado = cursor.fetchone()

        if resultado:
            fecha_actual, noPoliza_Actual = resultado
            
            cursor.execute("""
                UPDATE polizasIngresos
                SET fecha = ?, noPoliza = ?, banco = ?, importe = ?, nota = ?
                WHERE id = ?
            """, (nueva_fecha, nuevo_poliza, nuevo_banco, nuevo_importe, nueva_nota, id_registro))
        
            cursor.execute("""
                UPDATE detallePolizaIngreso
                SET fecha = ?, noPoliza = ?
                WHERE noPoliza = ? AND fecha = ?
            """, (nueva_fecha, nuevo_poliza, noPoliza_Actual, fecha_actual))
            
            for detalle in entradas_detalles:
                id = detalle["id"]
                nueva_clave = detalle["clave"].get().strip()
                abono_text = detalle["abono"].get().strip()
                if not abono_text:
                    continue
                try:
                    nuevo_abono = float(abono_text)
                except ValueError:
                    continue
            
                cursor.execute("""
                    UPDATE detallePolizaIngreso
                    SET clave = ?, abono = ?
                    WHERE id = ?
                """, (nueva_clave, nuevo_abono, id))
        
        conexion.commit()
        conexion.close()
        ventana_editar.destroy()
        mostrar_detalles_ingresos(frame_padre)
    
    # ✅ BOTONES ABAJO (puedes moverlos dentro del frame_scroll_general si quieres que también se desplacen)
    frame_botones = ctk.CTkFrame(frame_scroll_general, fg_color="transparent")
    frame_botones.pack(pady=(20, 10))
    ctk.CTkButton(frame_botones, text="Guardar cambios", fg_color="#008d62", hover_color="#2ca880", command=guardar).pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="Cancelar", fg_color="#d10d2f", hover_color="#d93954", command=ventana_editar.destroy).pack(side="left", padx=10)

def actualizar_estilo_tabla(tabla):
    modo = ctk.get_appearance_mode()
    estilo_act = "Dark.Treeview" if modo == "Dark" else "Light.Treeview"
    tabla.configure(style=estilo_act)  
    
def confirmar_generar_reporte():
    respuesta = messagebox.askokcancel("Información", "Está a punto de generar de nuevo el reporte de ingresos, asegurese de que los datos sean correctos")
    if respuesta:
        generar_reporte_xlwings()

def estilo_tabla():
    style = ttk.Style()
    style.theme_use("clam")  # Tema más flexible

    # Modo claro
    style.configure("Light.Treeview",
        background="white",
        foreground="black",
        fieldbackground="white",  # ¡Nuevo! Fondo de celdas
        rowheight=30,
        font=("Arial", 16)
    )
    
    # Modo oscuro
    style.configure("Dark.Treeview",
        background="#1e1e1e",
        foreground="white",
        fieldbackground="#1e1e1e",  # ¡Nuevo! Fondo de celdas
        rowheight=30,
        font=("Arial", 16)
    )

    # Heading (igual que antes, bien definido)
    style.configure("Light.Treeview.Heading",
        background="#f0f0f0",
        foreground="black",
        font=("Arial", 20, "bold")
    )
    style.configure("Dark.Treeview.Heading",
        background="#333333",
        foreground="white",
        font=("Arial", 20, "bold")
    )

    # Mapeo mejorado (incluye estado normal y selección)
    style.map("Light.Treeview",
        background=[("selected", "#cce5ff"), ("!selected", "white")], 
        foreground=[("selected", "black"), ("!selected", "black")]
    )
    style.map("Dark.Treeview",
        background=[("selected", "#3a3a3a"), ("!selected", "#1e1e1e")], 
        foreground=[("selected", "white"), ("!selected", "white")]
    )





                          
    

    
    