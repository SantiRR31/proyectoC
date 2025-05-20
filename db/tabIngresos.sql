CREATE TABLE polizasIngresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    noPoliza TEXT UNIQUE,
    banco TEXT,
    importe REAL,
    nota TEXT
);

CREATE TABLE detallePolizaIngreso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    noPoliza TEXT,
    clave TEXT,
    abono REAL,
    FOREIGN KEY (noPoliza) REFERENCES polizasIngresos(noPoliza)
);
