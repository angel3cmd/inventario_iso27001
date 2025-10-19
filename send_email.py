import smtplib
import os
from email.message import EmailMessage

def send_backup_email(file_path, recipient_email):
    msg = EmailMessage()
    msg['Subject'] = 'Backup Inventario ISO 27001'
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = recipient_email
    msg.set_content('Adjunto el backup generado automáticamente.')

    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_PASSWORD'))
        smtp.send_message(msg)
        print(f"Correo enviado a {recipient_email}")
