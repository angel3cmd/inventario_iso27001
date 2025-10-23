import sqlite3
import os

def init_db():
    db_path = 'data/inventario.db'
    if os.path.isdir(db_path):
        raise RuntimeError(f"Error: '{db_path}' es una carpeta, no un archivo de base de datos.")
    conn = sqlite3.connect(db_path)
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