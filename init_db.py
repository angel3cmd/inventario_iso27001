import sqlite3

conn = sqlite3.connect('inventario.db')
conn.execute("""
CREATE TABLE IF NOT EXISTS auditoria_envios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    archivo TEXT,
    destino TEXT
)
""")
conn.commit()
conn.close()
print("✅ Tabla auditoria_envios creada (si no existía).")
