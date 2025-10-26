import os
import sqlite3
import pandas as pd
from datetime import datetime

def exportar_excel():
    conn = sqlite3.connect('data/inventario.db')
    df = pd.read_sql_query("SELECT * FROM activos", conn)
    conn.close()

    ruta = os.path.join('static', 'exportados')
    os.makedirs(ruta, exist_ok=True)

    nombre_archivo = f"activos_exportados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(os.path.join(ruta, nombre_archivo), index=False)

    return nombre_archivo
