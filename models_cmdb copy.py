import sqlite3

DB_PATH = 'data/inventario.db'

def obtener_activos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activos")
    activos = cursor.fetchall()
    conn.close()
    return activos

def agregar_activo(nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO activos (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta))
    conn.commit()
    conn.close()

def buscar_activos(criterio):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM activos
        WHERE nombre LIKE ? OR tipo LIKE ? OR propietario LIKE ?
    """, (f'%{criterio}%', f'%{criterio}%', f'%{criterio}%'))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
