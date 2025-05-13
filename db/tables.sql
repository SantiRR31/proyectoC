CREATE TABLE IF NOT EXISTS 'partidasIngresos' (
    partida TEXT NOT NULL PRIMARY KEY,
    denominacion TEXT NOT NULL
);

INSERT INTO partidasIngresos (partida, denominacion) VALUES
("A001", "Acreditacion, Certificacion y Convalidacion de Estudios"),
("A002", "Expedición y Otorgamiento de Documentos Oficiales"),
("A003", "Exámenes"),
("A004", "Otros"),
("B001", "Cuotas de Cooperación Voluntaria"),
("B002", "Aportaciones, Cooperaciones y Donaciones al Plantel"),
("B003", "Beneficios"),
("B004", "Otros"),
("C001", "Servicios Médicos"),
("C002", "Servicios a Personas"),
("C003", "Servicios de Asesoría y Orientación"),
("C004", "Servicios de Mantenimiento"),
("C005", "Alquileres"),
("C006", "Otros"),
("D001", "Productos Derivadoe de la Actividad Agricola"),
("D002", "Productos Procesados"),
("D003", "Alimentos Procesados"),
("D004", "Productos Derivados de la Cunicultura"),
("D005", "Productos Derivados de la Actividad Ganadera"),
("D006", "Prod. Deriv. de las Activ. de Captura y Extracc. de Espec. Mar. Lacustres y Pluv."),
("D007", "Productos Derivados de la Actividad Apícola"),
("D008", "Productos Derivados de la Actividad Avícola"),
("D009", "Otros");

SELECT * FROM partidasIngresos;

. 
