
SELECT 
            substr(p.fecha, 1, 10) AS fecha,
            'DEPOSITO' AS descripcion,
            d.abono AS cargo,
            p.noPoliza
        FROM detallePolizaIngreso d
        JOIN polizasIngresos p ON d.noPoliza = p.noPoliza
        WHERE substr(p.fecha, 4, 2) = ? AND substr(p.fecha, 7, 4) = ?
        ORDER BY DATE(substr(p.fecha, 7, 4) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)) ASC