import sqlite3

def obtener_totales_depositos_por_poliza(mes_anio):
    conn = sqlite3.connect("prueba.db")
    cursor = conn.cursor()

    query = """
        SELECT 
            substr(p.fecha, 1, 10) AS fecha,
            'DEPOSITO' AS descripcion,
            SUM(d.abono) AS cargo,
            p.noPoliza
        FROM detallePolizaIngreso d
        JOIN polizasIngresos p ON d.noPoliza = p.noPoliza
        WHERE substr(p.fecha, 4, 2) = ? AND substr(p.fecha, 7, 4) = ?
        GROUP BY p.fecha, p.noPoliza
        ORDER BY DATE(substr(p.fecha, 7, 4) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)) ASC
    """

    mes = mes_anio.split('-')[1]
    anio = mes_anio.split('-')[0]

    cursor.execute(query, (mes, anio))
    resultados = cursor.fetchall()
    conn.close()

    print(f"Resultados para {mes_anio}:")
    for fila in resultados:
        print(f"Fecha: {fila[0]} | Descripción: {fila[1]} | Cargo: {fila[2]} | NoPoliza: {fila[3]}")

    return resultados

if __name__ == "__main__":
    obtener_totales_depositos_por_poliza("2025-06")
