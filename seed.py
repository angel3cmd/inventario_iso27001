import sqlite3

activos = [
    ("Servidor BD", "Hardware", "IT Admin", "CPD", "Confidencial", "Activo", "2025-01-15", "BD001"),
    ("CRM Cloud", "Software", "Comercial", "Azure", "Interna", "Activo", "2025-03-10", "CRM01"),
    ("Laptop Gerente", "Hardware", "Gerencia", "Oficina 3", "Confidencial", "Activo", "2025-02-20", "LTG01"),
    ("Manual ISO", "Documento", "Calidad", "SharePoint", "Pública", "Activo", "2025-04-01", "ISO01")
]

conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()
cursor.executemany('''
    INSERT INTO activos (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', activos)
conn.commit()
conn.close()
