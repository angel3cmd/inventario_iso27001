import sqlite3

DB_PATH = 'data/inventario.db'

def crear_tablas_cmdb():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT,
        telefono TEXT,
        departamento TEXT,
        puesto TEXT,
        ubicacion TEXT,
        fecha_ingreso TEXT,
        supervisor TEXT,
        usuario TEXT UNIQUE,
        clave TEXT,
        estado TEXT CHECK(estado IN ('activo', 'inactivo', 'baja'))
    )
    """)

    # Equipos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        tipo TEXT,
        marca TEXT,
        modelo TEXT,
        numero_serie TEXT,
        mac TEXT,
        ip TEXT,
        sistema_operativo TEXT,
        version_so TEXT,
        estado TEXT,
        ubicacion TEXT,
        usuario_id INTEGER,
        departamento TEXT,
        fecha_adquisicion TEXT,
        proveedor TEXT,
        garantia_hasta TEXT,
        costo REAL,
        clasificacion TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """)

    # Inmobiliario
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inmobiliario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        descripcion TEXT,
        ubicacion TEXT,
        numero_inventario TEXT,
        estado TEXT,
        fecha_adquisicion TEXT,
        proveedor TEXT,
        costo REAL,
        asignado_a TEXT
    )
    """)

    # Dispositivos de red
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dispositivos_red (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        marca TEXT,
        modelo TEXT,
        numero_serie TEXT,
        ip TEXT,
        mac TEXT,
        ubicacion TEXT,
        estado TEXT,
        firmware TEXT,
        fecha_instalacion TEXT,
        proveedor TEXT,
        contrato_soporte TEXT,
        configuracion TEXT
    )
    """)

    # Activos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        tipo TEXT,
        propietario TEXT,
        ubicacion TEXT,
        clasificacion TEXT,
        estado TEXT,
        fecha_alta TEXT,
        etiqueta TEXT
    )
    """)

    # Relaciones entre CIs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS relaciones_ci (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origen_tipo TEXT,
        origen_id INTEGER,
        destino_tipo TEXT,
        destino_id INTEGER,
        tipo_relacion TEXT,
        descripcion TEXT
    )
    """)

    # Auditoría de envíos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auditoria_envios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        archivo TEXT,
        destino TEXT
    )
    """)

    conn.commit()
    conn.close()
