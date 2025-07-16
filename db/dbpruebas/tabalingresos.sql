SELECT sql FROM sqlite_master WHERE type='table' AND name='polizasIngresos';
-- Ver las tablas existentes
.tables

CREATE TABLE detallePolizaIngreso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    noPoliza TEXT,
    clave TEXT,
    abono REAL, fecha TEXT,
    FOREIGN KEY (noPoliza) REFERENCES polizasIngresos(noPoliza)
)

CREATE TABLE polizasIngresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    noPoliza TEXT UNIQUE,
    banco TEXT,
    importe REAL,
    nota TEXT
)
DELETE FROM detallePolizaIngreso;

DELETE from polizasIngresos;

