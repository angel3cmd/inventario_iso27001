import sqlite3

def init_db():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
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
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            usuario TEXT PRIMARY KEY,
            clave TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO usuarios VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

def agregar_activo(nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta):
    if clasificacion not in ['Confidencial', 'Interna', 'Pública']:
        raise ValueError("Clasificación inválida según ISO 27001")
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activos (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta))
    conn.commit()
    conn.close()

def obtener_activos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activos')
    activos = cursor.fetchall()
    conn.close()
    return activos
