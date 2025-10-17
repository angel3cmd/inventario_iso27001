import pandas as pd
import sqlite3

def exportar_excel():
    conn = sqlite3.connect('inventario.db')
    df = pd.read_sql_query("SELECT * FROM activos", conn)
    df.to_excel("inventario_exportado.xlsx", index=False)
    conn.close()
