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

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    clave TEXT NOT NULL,
    rol TEXT NOT NULL
);

-- Tabla de auditoría de envíos
CREATE TABLE IF NOT EXISTS auditoria_envios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    archivo TEXT,
    destino TEXT
);

-- Tabla de relaciones entre elementos de configuración (CIs)
CREATE TABLE IF NOT EXISTS relaciones_ci (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origen_tipo TEXT NOT NULL,
    origen_id INTEGER NOT NULL,
    destino_tipo TEXT NOT NULL,
    destino_id INTEGER NOT NULL,
    tipo_relacion TEXT NOT NULL,
    descripcion TEXT
);
-- Tabla de configuración
CREATE TABLE IF NOT EXISTS configuracion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clave TEXT NOT NULL,
    valor TEXT NOT NULL
);

-- Tabla de reportes
CREATE TABLE IF NOT EXISTS reportes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    fecha TEXT NOT NULL,
    tipo TEXT
);

-- Tabla de integraciones
CREATE TABLE IF NOT EXISTS integraciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    estado TEXT NOT NULL
);

-- Índices para mejorar el rendimiento de las consultas
CREATE INDEX IF NOT EXISTS idx_activos_tipo ON activos(tipo);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_origen ON relaciones_ci(origen_tipo, origen_id);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_destino ON relaciones_ci(destino_tipo, destino_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_usuario ON usuarios(usuario);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_fecha ON auditoria_envios(fecha);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_destino ON auditoria_envios(destino);
CREATE INDEX IF NOT EXISTS idx_activos_propietario ON activos(propietario);
CREATE INDEX IF NOT EXISTS idx_activos_estado ON activos(estado);
CREATE INDEX IF NOT EXISTS idx_activos_clasificacion ON activos(clasificacion);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_tipo_relacion ON relaciones_ci(tipo_relacion);
CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_archivo ON auditoria_envios(archivo);
CREATE INDEX IF NOT EXISTS idx_activos_ubicacion ON activos(ubicacion);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_origen_id ON relaciones_ci(origen_id);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_destino_id ON relaciones_ci(destino_id);
CREATE INDEX IF NOT EXISTS idx_activos_fecha_alta ON activos(fecha_alta);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_descripcion ON relaciones_ci(descripcion);
CREATE INDEX IF NOT EXISTS idx_usuarios_clave ON usuarios(clave);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_id ON auditoria_envios(id);
CREATE INDEX IF NOT EXISTS idx_activos_id ON activos(id);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_id ON relaciones_ci(id);
CREATE INDEX IF NOT EXISTS idx_usuarios_id ON usuarios(id);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_fecha_archivo ON auditoria_envios(fecha, archivo);
CREATE INDEX IF NOT EXISTS idx_activos_nombre ON activos(nombre);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_origen_tipo_id ON relaciones_ci(origen_tipo, origen_id);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_destino_tipo_id ON relaciones_ci(destino_tipo, destino_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_usuario_rol ON usuarios(usuario, rol);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_destino_fecha ON auditoria_envios(destino, fecha);
CREATE INDEX IF NOT EXISTS idx_activos_tipo_estado ON activos(tipo, estado);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_tipo_relacion_descripcion ON relaciones_ci(tipo_relacion, descripcion);
CREATE INDEX IF NOT EXISTS idx_usuarios_rol_usuario ON usuarios(rol, usuario);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_archivo_destino ON auditoria_envios(archivo, destino);
CREATE INDEX IF NOT EXISTS idx_activos_propietario_ubicacion ON activos(propietario, ubicacion);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_origen_destino ON relaciones_ci(origen_tipo, origen_id, destino_tipo, destino_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_clave_rol ON usuarios(clave, rol);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_fecha_archivo_destino ON auditoria_envios(fecha, archivo, destino);
CREATE INDEX IF NOT EXISTS idx_activos_nombre_tipo ON activos(nombre, tipo);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_origen_tipo_destino_tipo ON relaciones_ci(origen_tipo, destino_tipo);
CREATE INDEX IF NOT EXISTS idx_usuarios_usuario_clave ON usuarios(usuario, clave);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_id_fecha ON auditoria_envios(id, fecha);
CREATE INDEX IF NOT EXISTS idx_activos_id_nombre ON activos(id, nombre);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_id_origen ON relaciones_ci(id, origen_tipo, origen_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_id_usuario ON usuarios(id, usuario);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_id_destino ON auditoria_envios(id, destino);
CREATE INDEX IF NOT EXISTS idx_activos_id_tipo ON activos(id, tipo);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_id_destino ON relaciones_ci(id, destino_tipo, destino_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_id_rol ON usuarios(id, rol);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_id_archivo ON auditoria_envios(id, archivo);
CREATE INDEX IF NOT EXISTS idx_activos_id_estado ON activos(id, estado);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_id_tipo_relacion ON relaciones_ci(id, tipo_relacion);
CREATE INDEX IF NOT EXISTS idx_usuarios_id_clave ON usuarios(id, clave);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_id_fecha_archivo ON auditoria_envios(id, fecha, archivo);
CREATE INDEX IF NOT EXISTS idx_activos_id_propietario ON activos(id, propietario);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_id_origen_destino ON relaciones_ci(id, origen_tipo, origen_id, destino_tipo, destino_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_id_usuario_rol ON usuarios(id, usuario, rol);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_id_destino_fecha ON auditoria_envios(id, destino, fecha);
CREATE INDEX IF NOT EXISTS idx_activos_id_clasificacion ON activos(id, clasificacion);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_id_tipo_relacion_descripcion ON relaciones_ci(id, tipo_relacion, descripcion);
CREATE INDEX IF NOT EXISTS idx_usuarios_id_clave_rol ON usuarios(id, clave, rol);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_id_archivo_destino ON auditoria_envios(id, archivo, destino);
CREATE INDEX IF NOT EXISTS idx_activos_id_ubicacion ON activos(id, ubicacion);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_id_origen_tipo_id ON relaciones_ci(id, origen_tipo, origen_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_id_usuario_clave ON usuarios(id, usuario, clave);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_id_fecha_archivo_destino ON auditoria_envios(id, fecha, archivo, destino);
CREATE INDEX IF NOT EXISTS idx_activos_id_nombre_tipo ON activos(id, nombre, tipo);
CREATE INDEX IF NOT EXISTS idx_relaciones_ci_id_origen_tipo_destino_tipo ON relaciones_ci(id, origen_tipo, destino_tipo);
CREATE INDEX IF NOT EXISTS idx_usuarios_id_usuario_clave_rol ON usuarios(id, usuario, clave, rol);
CREATE INDEX IF NOT EXISTS idx_auditoria_envios_id_fecha_archivo_destino ON auditoria_envios(id, fecha, archivo, destino);
-- Fin del archivo schema.sql
