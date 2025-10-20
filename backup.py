import os
import sqlite3
import pandas as pd
from datetime import datetime
from send_email import send_backup_email

# 🗂️ Crear carpetas si no existen
os.makedirs('data', exist_ok=True)
os.makedirs('backups', exist_ok=True)

def export_backup():
    db_path = 'data/inventario.db'
    if os.path.isdir(db_path):
        raise RuntimeError(f"❌ '{db_path}' es una carpeta, no un archivo de base de datos.")

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM activos", conn)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"backups/backup_inventario_{timestamp}.xlsx"
    df.to_excel(filename, index=False)
    conn.close()
    print(f"✅ Backup generado: {filename}")
    return filename

if __name__ == "__main__":
    # 📦 Generar respaldo
    backup_file = export_backup()

    # 📧 Enviar por correo
    recipient = os.getenv('EMAIL_RECIPIENT') or "tucorreo@ejemplo.com"
    if os.path.exists(backup_file):
        send_backup_email(backup_file, recipient)
    else:
        print(f"❌ Archivo no encontrado: {backup_file}")
