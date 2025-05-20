SELECT strftime('%Y-%m', 
       substr(fecha, 7) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)
      ) as mes_calculado,
       fecha as original
FROM polizasIngresos;