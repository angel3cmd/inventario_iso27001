import subprocess
import sqlite3
import os

print("🔄 Reiniciando sistema completo...")

# 🧱 Ejecutar init_db.py
print("\n--- Ejecutando init_db.py ---")
subprocess.run(["python", "init_db.py"])

# 🔐 Ejecutar init_key.py
print("\n--- Ejecutando init_key.py ---")
subprocess.run(["python", "init_key.py"])

# 📋 Verificar tablas creadas
db_path = "inventario.db"
if os.path.isdir(db_path):
    print(f"❌ Error: '{db_path}' es una carpeta, no un archivo de base de datos.")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        print("\n✅ Tablas encontradas:", tablas)
        conn.close()
    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {e}")
