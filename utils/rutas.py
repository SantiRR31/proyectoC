import os
import sys
import shutil
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

NOMBRE_APP = "GestorEgresosIngresos"
NOMBRE_BD = "prueba2.db"
NOMBRE_BD2 = "prueba.db"




def ruta_absoluta(ruta_relativa):
    """Devuelve la ruta absoluta, compatible con PyInstaller."""
    if getattr(sys, 'frozen', False):  # Si está empaquetado con PyInstaller
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)


# Cargar variables de entorno (.env)
dotenv_path = ruta_absoluta(".env")
load_dotenv(dotenv_path)

def obtener_ruta_appdata(nombre_archivo=""):
    ruta_base = os.path.join(os.environ["LOCALAPPDATA"], NOMBRE_APP)
    os.makedirs(ruta_base, exist_ok=True)
    return os.path.join(ruta_base, nombre_archivo) if nombre_archivo else ruta_base

def inicializar_base_datos():
    try:
        ruta_destino = obtener_ruta_appdata(NOMBRE_BD)
        if not os.path.exists(ruta_destino):
            ruta_origen = Path(ruta_absoluta(os.path.join("db", NOMBRE_BD)))
            if ruta_origen.exists():
                shutil.copy(ruta_origen, ruta_destino)
                print(f"[✓] Base de datos '{NOMBRE_BD}' copiada a: {ruta_destino}")
            else:
                print(f"[!] No se encontró la base de datos '{NOMBRE_BD}' en 'db'.")
            migrar_personal()
    except Exception as e:
        print(f"[✗] Error al copiar '{NOMBRE_BD}': {e}")

def inicializar_base_datos2():
    try:
        ruta_destino = obtener_ruta_appdata(NOMBRE_BD2)
        if not os.path.exists(ruta_destino):
            ruta_origen = Path(ruta_absoluta(NOMBRE_BD2))
            if ruta_origen.exists():
                shutil.copy(ruta_origen, ruta_destino)
                print(f"[✓] Base de datos '{NOMBRE_BD2}' copiada a: {ruta_destino}")
            else:
                print(f"[!] No se encontró la base de datos '{NOMBRE_BD2}' en el directorio actual.")
    except Exception as e:
        print(f"[✗] Error al copiar '{NOMBRE_BD2}': {e}")
from pathlib import Path

def obtener_carpeta_destino_segura(config):
    try:
        ruta = Path(config.get("carpeta_destino", "")).expanduser()
        ruta.mkdir(parents=True, exist_ok=True)
        return str(ruta)
    except Exception as e:
        print("⚠️ No se pudo acceder a la carpeta destino:", e)
        # Ruta local alternativa segura
        ruta_respaldo = Path(os.getcwd()) / "Cecati122" / "Polizas"
        ruta_respaldo.mkdir(parents=True, exist_ok=True)
        return str(ruta_respaldo)
    
def migrar_personal():
    from db.conexion import conectar
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
             SELECT name FROM sqlite_master WHERE type='table' AND name='personal';
        """)
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            # Crear tabla
            cursor.execute("""
                CREATE TABLE personal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombreCompleto TEXT NOT NULL,
                    rfc TEXT NOT NULL,
                    clave TEXT NOT NULL,
                    puesto TEXT
                );
            """)
            print("[✓] Tabla 'personal' creada")

        # Insertar registros
            cursor.executemany("""
                INSERT INTO personal (nombreCompleto, rfc, clave, puesto) VALUES (?, ?, ?, ?)
            """, [
                ('ANGELES PEREZ ROSA MARTHA', 'AEPR690905AR5', 'E096571', 'Instructor de estilismo'),
                ('GUILLEN VAZQUEZ MARIA ELENA', 'GUVE631104SS7', 'T03E031', 'Contadora'),
                ('HERNANDEZ DIAZ ELOISA', 'HEDE740925N98', 'A03E010', ''),
                ('HERRERA OLVERA MARIA LILIA', 'HEOL690625TK3', 'A03E031', ''),
                ('MALAGON AVILA LUIS FERNANDO', 'MAAL6710227247', 'E0965', 'Jefe de Capacitación'),
                ('MEJIA GONZALEZ FERNANDO', 'MEGF76705103D8', 'S01E07', 'Asistente de servicios en plantel'),
                ('MEJIA GONZALEZ ROGELIO', 'MEGR7110138P8', 'S01E07', 'Asistente de servicios en plantel'),
                ('MORENO VAZQUEZ JACQUELINE', 'MOVJ6810264V1', 'A03E01', '___ de apoyo'),
                ('SOLIS RUFINO MANUEL ALEJANDRO', 'SORM740702EX3', 'E0965', 'Instructor diseño gráfico'),
                ('DELGADO ARANA BERENICE', 'DEAB700330QJ9', 'E0965', 'Jefe del área de vinculación'),
                ('PEREZ ESTRADA MARISELA D.', 'PEEM6809257S5', 'T26E04', 'Trabajador social'),
                ('J. CUPERTINO SARMIENTO MERCADO', 'SAMJ8912182F9', 'E0965', 'Director'),
                ('EVA GUADALUPE MORALES GONZALEZ', 'MOGE680829431', 'E0965', 'Instructor de estilismo'),
                ('JONATHAN JESUS CRUZ MORALES', 'CUMJ931106A60', 'S01E07', 'Asistente de servicios en plantel'),
                ('URIEL ADOLFO MARTINEZ MARTINEZ', 'MAMU871111TH0', 'E0965', 'Instructor de alimentos y bebidas'),
                ('ANTONIO ALVAREZ CAMACHO', 'AACA750508K67', 'S01E07', 'Asistente de servicios en plantel'),
                ('HECTOR MARCOS ABREU LARA', 'AELH621118H69', 'E0965', 'Intructor de mecánica')
            ])
            print("[✓] Datos insertados en la tabla 'personal'")
        else:
            print("[✓] Tabla 'personal' ya existe, no se realizaron cambios")
            
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error en la migracion de personal: {e}")