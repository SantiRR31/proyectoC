CREATE TABLE polizasEgresos (
    id_poliza INTEGER PRIMARY KEY AUTOINCREMENT,
    no_poliza TEXT UNIQUE,         
    fecha DATE NOT NULL,
    monto REAL NOT NULL,
    nombre TEXT NOT NULL,
    tipo_pago TEXT NOT NULL,
    clave_ref TEXT ,
    denominacion TEXT,
    observaciones TEXT,
    no_cheque TEXT
);

create table if not exists detallePolizaEgreso (
    "id_poliza" intager not null,
    "CLAVE CUCoP" text not null,
    cargo real not null,
    FOREIGN KEY (id_poliza) REFERENCES polizasEgresos(id_poliza),
    FOREIGN KEY ("CLAVE CUCoP") REFERENCES partidasEgresos("CLAVE CUCoP")
);

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

drop table detallePolizaEgreso;
drop table polizasEgresos;

-- Renombre la tabla 
ALTER TABLE polizasEgresos RENAME TO polizasEgresos_old;
-- ver el sql usado para crear la tabla 
SELECT sql FROM sqlite_master WHERE type='table' AND name='polizasEgresos';
-- Ver las tablas existentes
.tables
-- 
select * from partidasEgresos;



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

SELECT "CLAVE CUCoP", "DESCRIPCIÓN", "PARTIDA ESPECÍFICA"
FROM partidasEgresos
WHERE "DESCRIPCIÓN" LIKE 'apo%'
UNION ALL
SELECT "CLAVE CUCoP", "DESCRIPCIÓN", "PARTIDA ESPECÍFICA"
FROM partidasEgresos
WHERE "DESCRIPCIÓN" LIKE '%apo%' AND "DESCRIPCIÓN" NOT LIKE 'apo%'

SELECT "PARTIDA ESPECÍFICA" FROM partidasEgresos WHERE "CLAVE CUCoP" = 21200038

INSERT INTO polizasEgresos (
    id_poliza, no_poliza, fecha, monto, nombre, tipo_pago, clave_ref, denominacion, observaciones
)
SELECT
    id_poliza, no_poliza, fecha, monto, nombre, tipo_pago, clave_ref, denominacion, observaciones
FROM polizasEgresos_old;

SELECT * FROM polizasEgresos;