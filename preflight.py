import os
import sqlite3
import subprocess
from dotenv import load_dotenv

print("🔍 Ejecutando verificación previa...")

# 1. Verificar .env
if not os.path.exists(".env"):
    print("❌ Falta el archivo .env")
else:
    print("✅ .env encontrado")
    load_dotenv()
    required_vars = ["FLASK_ENV", "SECRET_KEY"]
    for var in required_vars:
        if not os.getenv(var):
            print(f"⚠️ Variable faltante en .env: {var}")
        else:
            print(f"✅ Variable {var} definida")

# 2. Verificar secret.key
if not os.path.exists("secret.key"):
    print("❌ Falta secret.key")
else:
    print("✅ Clave secreta encontrada")

# 3. Verificar inventario.db
if not os.path.exists("inventario.db"):
    print("❌ Falta inventario.db")
else:
    try:
        conn = sqlite3.connect("inventario.db")
        conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print("✅ Base de datos válida")
        conn.close()
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")

# 4. Verificar carpeta backups
if not os.path.exists("backups"):
    print("❌ Falta carpeta backups/")
else:
    print("✅ Carpeta backups/ encontrada")

# 5. Verificar Docker
try:
    subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL)
    print("✅ Docker está instalado y corriendo")
except Exception:
    print("❌ Docker no está disponible o no está corriendo")

print("🧪 Verificación completa")

# 6. Verificar schema.sql
if not os.path.exists("schema.sql"):
    print("❌ Falta schema.sql")
else:
    print("✅ schema.sql encontrado")
