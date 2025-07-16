
SELECT pi.importe AS cargo, pi.fecha
FROM polizasIngresos pi
WHERE EXISTS (
    SELECT 1
    FROM detallePolizaIngreso dpi
    WHERE dpi.noPoliza = pi.noPoliza
      AND dpi.clave = '330'
)
ORDER BY pi.fecha;
