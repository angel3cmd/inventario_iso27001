import sqlite3

conn = sqlite3.connect("data/inventario.db")
cursor = conn.cursor()

try:
    cursor.execute("""
        INSERT INTO asignaciones_activos (activo_id, usuario_id, fecha_asignacion, observaciones)
        VALUES (?, ?, ?, ?)
    """, (1, 1, "2025-11-01", "Asignación inicial para pruebas"))
    conn.commit()
    print("✅ Asignación simulada insertada.")
except Exception as e:
    print("❌ Error al insertar asignación:", e)

conn.close()
