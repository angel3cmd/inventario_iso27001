import sqlite3
from flask import g

DB_PATH = 'data/inventario.db'

# 🔌 Conexión centralizada con row_factory
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

# ✅ Agregar activo con validación ISO
def agregar_activo(nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta):
    VALIDAS_ISO = ['Confidencial', 'Interno', 'Pública']
    if clasificacion not in VALIDAS_ISO:
        raise ValueError("Clasificación inválida según ISO 27001")

    campos = {
        'nombre': nombre,
        'tipo': tipo,
        'propietario': propietario,
        'ubicacion': ubicacion,
        'clasificacion': clasificacion,
        'estado': estado,
        'fecha_alta': fecha_alta
    }
    faltantes = [campo for campo, valor in campos.items() if not valor]
    if faltantes:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(faltantes)}")

    db = get_db()
    db.execute('''
        INSERT INTO activos (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta))
    db.commit()

# 📦 Obtener todos los activos
def obtener_activos():
    db = get_db()
    return db.execute('SELECT * FROM activos').fetchall()

# 🔍 Buscar activos por nombre, etiqueta o propietario
def buscar_activos(query=""):
    db = get_db()
    return db.execute("""
        SELECT * FROM activos
        WHERE nombre LIKE ? OR etiqueta LIKE ? OR propietario LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()

# 🔗 Agregar relación entre CIs
def agregar_relacion_ci(origen_tipo, origen_id, destino_tipo, destino_id, tipo_relacion, descripcion):
    TIPOS_RELACION = ['Depende de', 'Soporta a', 'Relacionado con']
    if tipo_relacion not in TIPOS_RELACION:
        raise ValueError("Tipo de relación inválido")

    db = get_db()
    db.execute("""
        INSERT INTO relaciones_ci (origen_tipo, origen_id, destino_tipo, destino_id, tipo_relacion, descripcion)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (origen_tipo, origen_id, destino_tipo, destino_id, tipo_relacion, descripcion))
    db.commit()

# 📋 Obtener todas las relaciones CI
def obtener_relaciones_ci():
    db = get_db()
    return db.execute("SELECT * FROM relaciones_ci").fetchall()

# 🛠️ Asignar y liberar activos

def asignar_activo_a_usuario(activo_id, usuario_id, fecha_asignacion, observaciones=""):
    db = get_db()

    asignado = db.execute("""
        SELECT * FROM asignaciones_activos
        WHERE activo_id = ? AND fecha_liberacion IS NULL
    """, (activo_id,)).fetchone()

    if asignado:
        raise ValueError("Este activo ya está asignado")

    db.execute("""
        INSERT INTO asignaciones_activos (activo_id, usuario_id, fecha_asignacion, observaciones)
        VALUES (?, ?, ?, ?)
    """, (activo_id, usuario_id, fecha_asignacion, observaciones))
    db.commit()

def liberar_activo(activo_id, fecha_liberacion):
    db = get_db()

    asignacion = db.execute("""
        SELECT * FROM asignaciones_activos
        WHERE activo_id = ? AND fecha_liberacion IS NULL
    """, (activo_id,)).fetchone()

    if not asignacion:
        raise ValueError("Este activo no está asignado actualmente")

    db.execute("""
        UPDATE asignaciones_activos
        SET fecha_liberacion = ?
        WHERE id = ?
    """, (fecha_liberacion, asignacion['id']))
    db.commit()

def obtener_asignaciones_activos():
    db = get_db()
    return db.execute("SELECT * FROM asignaciones_activos").fetchall()

def obtener_asignacion_activo(activo_id):
    db = get_db()
    return db.execute("""
        SELECT * FROM asignaciones_activos
        WHERE activo_id = ? AND fecha_liberacion IS NULL
    """, (activo_id,)).fetchone()

def obtener_activo_por_id(activo_id):
    db = get_db()
    return db.execute("SELECT * FROM activos WHERE id = ?", (activo_id,)).fetchone()

def obtener_activos_disponibles():
    db = get_db()
    return db.execute("""
        SELECT * FROM activos
        WHERE id NOT IN (
            SELECT activo_id FROM asignaciones_activos
            WHERE fecha_liberacion IS NULL
        )
    """).fetchall()

def liberar_activo(activo_id, fecha_liberacion):
    db = get_db()

    asignacion = db.execute("""
        SELECT * FROM asignaciones_activos
        WHERE activo_id = ? AND fecha_liberacion IS NULL
    """, (activo_id,)).fetchone()

    if not asignacion:
        raise ValueError("Este activo no está asignado actualmente")

    db.execute("""
        UPDATE asignaciones_activos
        SET fecha_liberacion = ?
        WHERE id = ?
    """, (fecha_liberacion, asignacion['id']))
    db.commit()

def obtener_activos_asignados_a_usuario(usuario_id):
    db = get_db()
    return db.execute("""
        SELECT a.*, aa.fecha_asignacion
        FROM activos a
        JOIN asignaciones_activos aa ON a.id = aa.activo_id
        WHERE aa.usuario_id = ? AND aa.fecha_liberacion IS NULL
    """, (usuario_id,)).fetchall()

def obtener_historial_asignaciones_activo(activo_id):
    db = get_db()
    return db.execute("""
        SELECT aa.*, u.nombre AS usuario_nombre
        FROM asignaciones_activos aa
        JOIN usuarios u ON aa.usuario_id = u.id
        WHERE aa.activo_id = ?
        ORDER BY fecha_asignacion DESC
    """, (activo_id,)).fetchall()
