import sqlite3

def obtener_totales_ingresos_debug(mes_anio):
    conn = sqlite3.connect("prueba.db")  # Ruta según tu caso real
    cursor = conn.cursor()
    cursor.execute("""
        SELECT clave, SUM(abono)
        FROM detallePolizaIngreso
        WHERE substr(fecha, 4, 2) = ? AND substr(fecha, 7, 4) = ?
        GROUP BY clave
        ORDER BY clave;
    """, (mes_anio.split('-')[1], mes_anio.split('-')[0]))
    resultados = cursor.fetchall()
    conn.close()
    
    print(f"Resultados para {mes_anio}:")
    for fila in resultados:
        print(f"Clave: {fila[0]} | Total: {fila[1]}")
    
    return resultados

# Ejemplo de ejecución manual
if __name__ == "__main__":
    obtener_totales_ingresos_debug("2025-07")

