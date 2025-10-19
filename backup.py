import os
import sqlite3
import pandas as pd
from datetime import datetime

def export_backup():
    conn = sqlite3.connect('inventario.db')
    df = pd.read_sql_query("SELECT * FROM activos", conn)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"/app/backups/backup_inventario_{timestamp}.xlsx"
    df.to_excel(filename, index=False)
    conn.close()
    print(f"Backup generado: {filename}")

if __name__ == "__main__":
    export_backup()
from send_email import send_backup_email
recipient = os.getenv('EMAIL_RECIPIENT')
send_backup_email(filename, recipient)
