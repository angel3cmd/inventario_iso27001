import sqlite3

# Conecta a la base de datos correcta
conn = sqlite3.connect("data/inventario.db")
cursor = conn.cursor()

# Ejecuta el ALTER TABLE
try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN nombre TEXT NOT NULL DEFAULT 'Sin nombre'")
    conn.commit()
    print("✅ Columna 'nombre' agregada correctamente a la tabla 'usuarios'.")
except sqlite3.OperationalError as e:
    print("⚠️ Error:", e)

conn.close()
