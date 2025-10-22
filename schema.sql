-- Tabla de activos
CREATE TABLE IF NOT EXISTS activos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    propietario TEXT NOT NULL,
    ubicacion TEXT NOT NULL,
    clasificacion TEXT NOT NULL,
    estado TEXT NOT NULL,
    fecha_alta TEXT NOT NULL,
    etiqueta TEXT
);

-- Tabla de auditoría de envíos
CREATE TABLE IF NOT EXISTS auditoria_envios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    archivo TEXT,
    destino TEXT
);

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    clave TEXT NOT NULL,
    rol TEXT NOT NULL
);
