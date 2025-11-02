import sqlite3

DB_PATH = "data/inventario.db"

usuarios_simulados = [
    (1, 'admin', 'Administrador General', 'admin123', 'admin'),
    (2, 'auditor', 'Auditor de Seguridad', 'auditor123', 'auditor'),
    (3, 'operador', 'Operador Técnico', 'operador123', 'operador')
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for usuario in usuarios_simulados:
    try:
        cursor.execute("""
            INSERT INTO usuarios (id, usuario, nombre, clave, rol)
            VALUES (?, ?, ?, ?, ?)
        """, usuario)
    except sqlite3.IntegrityError:
        print(f"⚠️ El usuario '{usuario[1]}' ya existe, se omitió.")
    else:
        print(f"✅ Usuario '{usuario[1]}' insertado.")

conn.commit()
conn.close()
print("🏁 Inserción de usuarios simulados completada.")
