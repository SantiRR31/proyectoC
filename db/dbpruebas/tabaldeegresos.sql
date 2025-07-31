CREATE TABLE polizasEgresos(
    id_poliza INTEGER PRIMARY KEY AUTOINCREMENT,
    no_poliza TEXT UNIQUE,         
    fecha DATE NOT NULL,
    monto REAL NOT NULL,
    nombre TEXT NOT NULL,
    tipo_pago TEXT NOT NULL,
    clave_ref TEXT,
    denominacion TEXT,
    observaciones TEXT,
    no_cheque TEXT,
    estado TEXT  
);



CREATE TABLE detallePolizaEgreso (
    id_poliza INTEGER NOT NULL,
    "CLAVE CUCoP" INTEGER NOT NULL,
    cargo REAL NOT NULL,
    "PARTIDA ESPECÍFICA" INTEGER NOT NULL,
    FOREIGN KEY (id_poliza) REFERENCES polizasEgresos(id_poliza) ON DELETE CASCADE,
    FOREIGN KEY ("CLAVE CUCoP") REFERENCES partidasEgresos("CLAVE CUCoP")
);


INSERT INTO detallePolizaEgreso (id_poliza, "CLAVE CUCoP", cargo, "PARTIDA ESPECÍFICA")
SELECT id_poliza, "CLAVE CUCoP", cargo, "PARTIDA ESPECÍFICA"
FROM detallePolizaEgreso_old;


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
drop table ;

-- Renombre la tabla 
ALTER TABLE detallePolizaEgreso RENAME TO detallePolizaEgreso_old;
-- ver el sql usado para crear la tabla 
SELECT sql FROM sqlite_master WHERE type='table' AND name='detallePolizaEgreso';
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
FROM partidasEgresos
WHERE "CABM ACTUALIZADO" = 'i';

DELETE FROM partidasEgresos_old
WHERE "CABM ACTUALIZADO" = 'i';

select "CLAVE CUCoP", COUNT(*) AS cantidad
FROM partidasEgresos
GROUP BY "CLAVE CUCoP"
HAVING cantidad > 1;

SELECT *
FROM partidasEgresos;

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


drop table partidasEgresos_old;

drop table polizasEgresos;


CREATE TABLE detallePolizaEgreso (
    id_poliza INTEGER NOT NULL,
    "CLAVE CUCoP" INTEGER NOT NULL,
    cargo REAL NOT NULL,
    "PARTIDA ESPECÍFICA" INTEGER NOT NULL,
    FOREIGN KEY (id_poliza) REFERENCES polizasEgresos_old(id_poliza),
    FOREIGN KEY ("CLAVE CUCoP") REFERENCES partidasEgresos("CLAVE CUCoP")
);

INSERT INTO detallePolizaEgreso (id_poliza, "CLAVE CUCoP", cargo, "PARTIDA ESPECÍFICA")
SELECT 
    d.id_poliza,
    d."CLAVE CUCoP",
    d.cargo,
    p."PARTIDA ESPECÍFICA"
FROM 
    detallePolizaEgreso_old d
    JOIN partidasEgresos p ON d."CLAVE CUCoP" = p."CLAVE CUCoP";


-- Consulta para obtener las pólizas de egresos del mes 

SELECT fecha, no_poliza, monto, id_poliza
FROM polizasEgresos
WHERE strftime('%Y-%m', 
    substr(fecha, 7) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)
) = '2025-06';

-- consulta para obtener partidas especificas unicas 

SELECT DISTINCT d."PARTIDA ESPECÍFICA"
FROM detallePolizaEgreso d
JOIN polizasEgresos p ON d.id_poliza = p.id_poliza
WHERE strftime('%Y-%m', 
    substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
) = '2025-06'
ORDER BY d."PARTIDA ESPECÍFICA";


SELECT "PARTIDA ESPECÍFICA", SUM(cargo)
FROM detallePolizaEgreso
WHERE id_poliza = 2
GROUP BY "PARTIDA ESPECÍFICA";
.tables

SELECT id_poliza, "PARTIDA ESPECÍFICA", cargo FROM detallePolizaEgreso;

select * from detallePolizaEgreso;
SELECT 
    p.id_poliza, 
    p.no_poliza, 
    p.fecha, 
    p.monto, 
    d."PARTIDA ESPECÍFICA", 
    d.cargo
WHERE 
    p.id_poliza = 1



INSERT INTO partidasEgresos (
    "CABM ACTUALIZADO",
    "TIPO",
    "PARTIDA ESPECÍFICA",
    "CLAVE CUCoP",
    "DESCRIPCIÓN",
    "NIVEL",
    "CABM ANTERIOR",
    "UNIDAD  DE MEDIDA (sugerida)"
) VALUES
('120', 1, 120, 120, 'Deudores diversos', 1, NULL, NULL),
('330', 1, 120, 330, 'Acreedores diversos', 1, NULL, NULL);


select * from partidasEgresos 
where "CLAVE CUCoP" = 330;


select * from detallePolizaEgreso
where id_poliza = 9;


UPDATE detallePolizaEgreso
SET "PARTIDA ESPECÍFICA" = 120
WHERE id_poliza = 9 AND "CLAVE CUCoP" = 120;

UPDATE detallePolizaEgreso
SET "CLAVE CUCoP" = 33300005, "PARTIDA ESPECÍFICA" = 33303
WHERE id_poliza = 11;


select * from polizasEgresos

UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'ene.', 'ene');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'feb.', 'feb');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'mar.', 'mar');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'abr.', 'abr');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'may.', 'may');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'jun.', 'jun');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'jul.', 'jul');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'ago.', 'ago');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'sep.', 'sep');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'oct.', 'oct');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'nov.', 'nov');
UPDATE polizasEgresos SET no_poliza = REPLACE(no_poliza, 'dic.', 'dic');



INSERT INTO partidasEgresos (
    "CABM ACTUALIZADO",
    "TIPO",
    "PARTIDA ESPECÍFICA",
    "CLAVE CUCoP",
    "DESCRIPCIÓN",
    "NIVEL",
    "CABM ANTERIOR",
    "UNIDAD  DE MEDIDA (sugerida)"
) VALUES
('37504', 3, 37504, 37504, 'Viaticos nacionales para servidores publicos en el sesempeño de funciones oficiales', 3, NULL, NULL),
('37500004', 4, 37504, 37500004, 'Viaticos nacionales para servidores publicos en el sesempeño de funciones oficiales', 4, NULL, NULL);


SELECT d."PARTIDA ESPECÍFICA", SUM(d.cargo)
FROM detallePolizaEgreso d
JOIN polizasEgresos po ON d.id_poliza = po.id_poliza
WHERE strftime('%Y-%m', substr(po.fecha, 7) || '-' || substr(po.fecha, 4, 2) || '-' || substr(po.fecha, 1, 2)) = '2025-04'
GROUP BY d."PARTIDA ESPECÍFICA";


SELECT 
    p.id_poliza,
    p.no_poliza,
    p.fecha,
    p.monto,
    p.nombre,
    p.tipo_pago,
    p.clave_ref,
    p.denominacion,
    p.observaciones,
    p.no_cheque,
    d."CLAVE CUCoP",
    d."PARTIDA ESPECÍFICA",
    d.cargo
FROM polizasEgresos p
JOIN detallePolizaEgreso d ON p.id_poliza = d.id_poliza
WHERE strftime('%Y-%m', 
    substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
) = '2025-06'
ORDER BY p.id_poliza, d."PARTIDA ESPECÍFICA";


SELECT * from polizasEgresos as p
WHERE strftime('%Y-%m', 
    substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
) = '2025-06'



-- 1. Borrar de detallePolizaEgreso todas las partidas de las pólizas del mes
DELETE FROM detallePolizaEgreso
WHERE id_poliza IN (
    SELECT id_poliza
    FROM polizasEgresos
    WHERE strftime('%Y-%m', 
        substr(fecha, 7) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)
    ) = '2025-06'
);

-- 2. Borrar las pólizas del mes
DELETE FROM polizasEgresos
WHERE strftime('%Y-%m', 
    substr(fecha, 7) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)
) = '2025-06';



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
VALUES (
    'P3920209202',
    2,
    39202,
    39202,
    'Otros impuestos y derechos',
    4,
    NULL,
    'Servicio'
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
VALUES (
    'C3920200001',
    2,
    39202,
    39202001,
    'Otros impuestos y derechos',
    5,
    NULL,
    'Servicio'
);



INSERT INTO polizasEgresos (
    id_poliza,
    no_poliza,
    fecha,
    monto,
    nombre,
    tipo_pago,
    clave_ref,
    denominacion,
    observaciones,
    no_cheque,
    estado
)
SELECT 
    id_poliza,
    no_poliza,
    fecha,
    monto,
    nombre,
    tipo_pago,
    clave_ref,
    denominacion,
    observaciones,
    no_cheque,
    'activo' AS estado
FROM polizasEgresos_old;



select * from polizasEgresos;


SELECT d.cargo, p.fecha, p.no_poliza
FROM detallePolizaEgreso d
JOIN polizasEgresos p ON d.id_poliza = p.id_poliza
WHERE d."PARTIDA ESPECÍFICA" = 120
  AND strftime('%Y-%m', substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)) = '2025-06'


SELECT pi.importe as cargo , pi.fecha 
from polizasIngresos pi
where exists (
    SELECT 1
    FROM detallePolizaIngreso dpi
    WHERE dpi.id_poliza = pi.id_poliza
      AND dpi."PARTIDA ESPECÍFICA" = 120
)
  AND strftime('%Y-%m', substr(pi.fecha, 7) || '-' || substr(pi.fecha, 4, 2) || '-' || substr(pi.fecha, 1, 2)) = '2025-06';

SELECT 
    p.fecha,
    p.nombre,
    p.tipo_pago,
    p.no_cheque,
    p.monto
FROM polizasEgresos p
WHERE strftime('%Y-%m', 
    substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
) = '2025-06';


select * from polizasEgresos
where strftime('%Y-%m', 
    substr(fecha, 7) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)
) = '2025-06';


update polizasEgresos
set tipo_pago = 'TRANSF. ELECTRÓNICA'
where id_poliza = 36;

SELECT p.fecha, SUM(d.abono) as total_abono
    FROM detallePolizaIngreso d
    JOIN polizasIngresos p ON d.noPoliza = p.noPoliza
    WHERE substr(p.fecha, 7, 4) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2) >= '2025-06'
        AND substr(p.fecha, 7, 4) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2) < '2025-06'


DELETE from detallePolizaEgreso
where id_poliza = "03/jul./2025";


DELETE FROM detallePolizaEgreso
WHERE typeof(id_poliza) != 'integer';


