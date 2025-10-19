import sqlite3
import os

print("🧱 Inicializando base de datos...")

if not os.path.exists("schema.sql"):
    print("❌ No se encontró schema.sql")
    exit(1)

try:
    conn = sqlite3.connect("inventario.db")
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("✅ inventario.db creada con schema.sql")
except Exception as e:
    print(f"❌ Error al inicializar la base de datos: {e}")
    exit(1)
