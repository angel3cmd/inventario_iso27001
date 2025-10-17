import sqlite3

def obtener_metricas():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM activos")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM activos WHERE clasificacion='Confidencial'")
    confidencial = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM activos WHERE propietario IS NULL OR propietario=''")
    sin_propietario = cursor.fetchone()[0]
    conn.close()
    return {
        "total": total,
        "confidencial": confidencial,
        "sin_propietario": sin_propietario
    }
