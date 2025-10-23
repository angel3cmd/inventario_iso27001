import sqlite3

def agregar_activo(nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta):
    # Validar clasificación
    if clasificacion not in ['Confidencial', 'Interna', 'Pública']:
        raise ValueError("Clasificación inválida según ISO 27001")

    # Validar campos obligatorios
    campos = {
        'nombre': nombre,
        'tipo': tipo,
        'propietario': propietario,
        'ubicacion': ubicacion,
        'clasificacion': clasificacion,
        'estado': estado,
        'fecha_alta': fecha_alta
    }
    faltantes = [campo for campo, valor in campos.items() if not valor]
    if faltantes:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(faltantes)}")

    # Insertar en la base de datos
    conn = sqlite3.connect('data/inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activos (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta))
    conn.commit()
    conn.close()

def obtener_activos():
    conn = sqlite3.connect('data/inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activos')
    activos = cursor.fetchall()
    conn.close()
    return activos
