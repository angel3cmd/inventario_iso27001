import sqlite3
from datetime import datetime

conn = sqlite3.connect("data/inventario.db")
cursor = conn.cursor()

print("🚀 Insertando datos de prueba...")

# Usuarios
usuarios = [
    ("admin", "admin123", "Administrador"),
    ("jlopez", "pass456", "Auditor"),
    ("mgarcia", "clave789", "Usuario"),
]
cursor.executemany("INSERT INTO usuarios (usuario, clave, rol) VALUES (?, ?, ?)", usuarios)

# Activos
activos = [
    ("Laptop Dell", "Equipo", "mgarcia", "CDMX", "Confidencial", "Activo", "2025-10-01", "DL-001"),
    ("Router Cisco", "Red", "admin", "CDMX", "Interna", "Activo", "2025-09-15", "RT-002"),
    ("Monitor LG", "Equipo", "jlopez", "CDMX", "Pública", "Inactivo", "2025-08-20", "MN-003"),
]
cursor.executemany("""
    INSERT INTO activos (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", activos)

# Auditoría
auditorias = [
    (datetime.now().isoformat(), "respaldo_octubre.zip", "OneDrive"),
    (datetime.now().isoformat(), "export_activos.csv", "Correo"),
]
cursor.executemany("INSERT INTO auditoria_envios (fecha, archivo, destino) VALUES (?, ?, ?)", auditorias)

# Relaciones entre CIs
relaciones = [
    ("activo", 1, "usuario", 3, "asignado_a", "Laptop Dell asignada a mgarcia"),
    ("activo", 2, "activo", 1, "depende_de", "Router Cisco conecta Laptop Dell"),
    ("activo", 3, "usuario", 2, "asignado_a", "Monitor LG asignado a jlopez"),
]
cursor.executemany("""
    INSERT INTO relaciones_ci (origen_tipo, origen_id, destino_tipo, destino_id, tipo_relacion, descripcion)
    VALUES (?, ?, ?, ?, ?, ?)
""", relaciones)

conn.commit()
conn.close()
print("✅ Datos cargados correctamente.")
