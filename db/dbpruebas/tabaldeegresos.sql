CREATE table if not exists polizasEgresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT not null,
    numero_poliza text not null UNIQUE,
    nombre TEXT not null,
    cargo_total REAL not null,
    tipo_pago TEXT NOT NULL CHECK (tipo_pago IN ('Efectivo', 'Cheque', 'Transferencia', 'Tarjeta de Crédito', 'Tarjeta de Débito')),
    observaciones TEXT,
);

create table if not exists detallePolizaEgreso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poliza_id intager not null,ytf
    clave_partida text not null,
    cargo real not null,
    FOREIGN KEY (poliza_id) REFERENCES polizasEgresos(id),
    FOREIGN KEY (clave_partida) REFERENCES partidasPresupuestarias(clave_partida)


);


-- Renombre la tabla 
ALTER TABLE partidasEgresos_old RENAME TO partidasEgresos_old;
-- ver el sql usado para crear la tabla 
SELECT sql FROM sqlite_master WHERE type='table' AND name='partidasEgresos';
-- Ver las tablas existentes
.tables
-- 
select * from partidasEgresos;

CREATE TABLE partidasEgresos (
    "CABM ACTUALIZADO" TEXT PRIMARY KEY,
    "TIPO" INTEGER,
    "PARTIDA ESPECÍFICA" INTEGER,
    "CLAVE CUCoP" INTEGER UNIQUE,
    "DESCRIPCIÓN" TEXT,
    "NIVEL" INTEGER,
    "CABM ANTERIOR" TEXT,
    "UNIDAD  DE MEDIDA (sugerida)" TEXT
);


INSERT INTO partidasEgresos (
    "CABM ACTUALIZADO",
    "TIPO",
    "PARTIDA ESPECÍFICA",
    "CLAVE CUCoP",
    "DESCRIPCIÓN",
    "NIVEL",
    "CABM ANTERIOR",
    "UNIDAD  DE MEDIDA (sugerida)"
)
SELECT
    "CABM ACTUALIZADO",
    "TIPO",
    "PARTIDA ESPECÍFICA",
    "CLAVE CUCoP",
    "DESCRIPCIÓN",
    "NIVEL",
    "CABM ANTERIOR",
    "UNIDAD  DE MEDIDA (sugerida)"
FROM partidasEgresos_old;

SELECT "CABM ACTUALIZADO", COUNT(*) AS cantidad
FROM partidasEgresos_old
GROUP BY "CABM ACTUALIZADO"
HAVING cantidad > 1;

SELECT *
FROM partidasEgresos_old
WHERE "CABM ACTUALIZADO" = 'i';

DELETE FROM partidasEgresos_old
WHERE "CABM ACTUALIZADO" = 'i';

select "CLAVE CUCoP", COUNT(*) AS cantidad
FROM partidasEgresos
GROUP BY "CLAVE CUCoP"
HAVING cantidad > 1;

SELECT *
FROM partidasEgresos_OLD
WHERE "CLAVE CUCoP" IS NULL;

DELETE FROM partidasEgresos_old
WHERE "CABM ACTUALIZADO" = 'j';

update partidasEgresos_old
set "CLAVE CUCoP" = 57700004
where "CABM ACTUALIZADO" = 'I5770100005'; 

select * 
from partidasEgresos_old
where "CLAVE CUCoP" = 57700004;

select * from partidasEgresos

drop table partidasEgresos

select * from partidasEgresos



SELECT 
    "DESCRIPCIÓN",
    COUNT(*) AS cantidad
FROM 
    partidasEgresos
GROUP BY 
    "DESCRIPCIÓN"
HAVING 
    COUNT(*) > 1;



