import sqlite3
import os

DB_PATH = "data/inventario.db"
SCHEMA_PATH = "schema.sql"

print("🧱 Inicializando base de datos...")

# Crear carpeta data si no existe
os.makedirs("data", exist_ok=True)

# Eliminar base anterior si existe
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("🧹 inventario.db anterior eliminada")

# Validar existencia y contenido de schema.sql
if not os.path.exists(SCHEMA_PATH):
    print("❌ No se encontró schema.sql")
    exit(1)

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    sql_script = f.read()
    if "CREATE TABLE" not in sql_script:
        print("❌ El archivo schema.sql no contiene definiciones de tablas")
        exit(1)

# Crear base de datos
try:
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(sql_script)
    conn.commit()
    print("✅ inventario.db creada con schema.sql")
except Exception as e:
    print(f"❌ Error al inicializar la base de datos: {e}")
    exit(1)

# Verificar tablas críticas
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = set(row[0] for row in cursor.fetchall())
esperadas = {
    "activos", "usuarios", "auditoria_envios",
    "relaciones_ci", "configuracion", "reportes"
}
faltantes = esperadas - tablas
if faltantes:
    print(f"⚠️ Faltan tablas: {', '.join(faltantes)}")
else:
    print("✅ Todas las tablas críticas están presentes.")

# Insertar datos simulados
try:
    cursor.execute("INSERT INTO usuarios (usuario, nombre, clave, rol) VALUES (?, ?, ?, ?)",
               ("admin", "Administrador General", "admin123", "admin"))
    cursor.execute("INSERT INTO configuracion (clave, valor) VALUES (?, ?)", ("idioma", "es"))
    cursor.execute("INSERT INTO configuracion (clave, valor) VALUES (?, ?)", ("tema", "oscuro"))
    cursor.execute("""
        INSERT INTO activos (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("Servidor A", "Hardware", "Miguel", "Sala 1", "Confidencial", "Activo", "2025-10-31", "SRV-A"))
    cursor.execute("""
        INSERT INTO auditoria_envios (fecha, archivo, destino)
        VALUES (?, ?, ?)
    """, ("2025-10-31", "informe.pdf", "auditoria@empresa.com"))
    cursor.execute("""
        INSERT INTO reportes (nombre, fecha, tipo)
        VALUES (?, ?, ?)
    """, ("Reporte mensual", "2025-10-01", "Financiero"))
    conn.commit()
    print("📦 Datos simulados insertados.")
except Exception as e:
    print(f"⚠️ Error al insertar datos simulados: {e}")

conn.close()
print("🏁 Inicialización completa.")
