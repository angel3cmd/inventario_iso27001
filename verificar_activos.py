import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()
cursor.execute("SELECT id, nombre, tipo, propietario FROM activos")
registros = cursor.fetchall()
print(f"🔍 Total de activos encontrados: {len(registros)}")
for r in registros:
    print(r)
conn.close()
