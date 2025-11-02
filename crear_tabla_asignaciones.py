import sqlite3

conn = sqlite3.connect("data/inventario.db")
cursor = conn.cursor()

try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asignaciones_activos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activo_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            fecha_asignacion TEXT NOT NULL,
            fecha_liberacion TEXT,
            observaciones TEXT,
            FOREIGN KEY (activo_id) REFERENCES activos(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)
    conn.commit()
    print("✅ Tabla 'asignaciones_activos' creada correctamente.")
except Exception as e:
    print("❌ Error al crear la tabla:", e)

conn.close()
