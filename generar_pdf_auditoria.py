from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import sqlite3
from datetime import datetime

def generar_pdf(path='auditoria_backups.pdf'):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.execute("SELECT fecha, archivo, destino FROM auditoria_envios ORDER BY fecha DESC")
    registros = cursor.fetchall()
    conn.close()

    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(50, 800, "Auditoría de Backups - ISO 27001")
    c.drawString(50, 785, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = 750
    for fecha, archivo, destino in registros:
        c.drawString(50, y, f"{fecha} | {archivo} | {destino}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 800

    c.save()
    return path
