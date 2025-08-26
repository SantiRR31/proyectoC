CREATE TABLE detalleIngresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    noPoliza TEXT NOT NULL,
    clave TEXT NOT NULL,
    abono REAL NOT NULL,
    fecha TEXT NOT NULL
);

CREATE TABLE polizasIngresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    noPoliza TEXT NOT NULL,
    fecha TEXT NOT NULL,
    banco TEXT NOT NULL,
    importe REAL NOT NULL,
    nota TEXT
);

CREATE TABLE partidasIngresos (
    partida TEXT PRIMARY KEY,
    denominacion TEXT NOT NULL
);