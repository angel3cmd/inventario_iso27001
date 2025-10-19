import os
import csv
import hashlib
import sqlite3
from io import StringIO
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, send_file, Response
from models import init_db, agregar_activo, obtener_activos
from auth import login_required, autenticar, es_admin, obtener_rol
from dashboard import obtener_metricas
from export import exportar_excel
from decrypt_file import decrypt_file
from generar_pdf_auditoria import generar_pdf

# 🔧 Configuración inicial
load_dotenv()
app = Flask(__name__)
from config import config_by_name
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config_by_name[env])
init_db()

# 🔐 Crear tabla auditoria_envios si no existe
conn = sqlite3.connect('inventario.db')
conn.execute("""
CREATE TABLE IF NOT EXISTS auditoria_envios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    archivo TEXT,
    destino TEXT
)
""")
conn.commit()
conn.close()

# 🏠 Panel principal con navegación por rol
@app.route('/home')
@login_required
def home():
    return render_template('home.html', rol=session.get('rol'))

# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if autenticar(usuario, clave):
            session['usuario'] = usuario
            session['rol'] = obtener_rol(usuario)
            return redirect('/home')
    return render_template('login.html')

# 🔓 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# 🏷️ Inventario
@app.route('/')
@login_required
def index():
    activos = obtener_activos()
    return render_template('index.html', activos=activos)

@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    agregar_activo(**request.form)
    return redirect('/')

# 📊 Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    metricas = obtener_metricas()
    return render_template('dashboard.html', metricas=metricas)

# 📤 Exportar Excel
@app.route('/exportar')
@login_required
def exportar():
    exportar_excel()
    return redirect('/')

# 🔁 Restaurar backup cifrado
@app.route('/restaurar')
@login_required
def listar_backups():
    archivos = [f for f in os.listdir('backups') if f.endswith('.enc')]
    return render_template('restaurar.html', archivos=archivos)

@app.route('/restaurar/<nombre>')
@login_required
def restaurar(nombre):
    encrypted_path = os.path.join('backups', nombre)
    output_path = os.path.join('backups', 'restaurado_' + nombre.replace('.enc', '.xlsx'))

    if not os.path.exists(encrypted_path):
        return "Archivo no encontrado", 404

    decrypt_file(encrypted_path, output_path)

    conn = sqlite3.connect('inventario.db')
    conn.execute("INSERT INTO auditoria_envios (fecha, archivo, destino) VALUES (?, ?, ?)",
                 (datetime.now().isoformat(), os.path.basename(output_path), 'restauración local'))
    conn.commit()
    conn.close()

    return send_file(output_path, as_attachment=True)

# 🧾 Auditoría con filtros
@app.route('/auditoria', methods=['GET', 'POST'])
@login_required
def ver_auditoria():
    filtro_fecha = request.form.get('fecha')
    filtro_destino = request.form.get('destino')

    query = "SELECT fecha, archivo, destino FROM auditoria_envios WHERE 1=1"
    params = []

    if filtro_fecha:
        query += " AND fecha LIKE ?"
        params.append(f"%{filtro_fecha}%")
    if filtro_destino:
        query += " AND destino LIKE ?"
        params.append(f"%{filtro_destino}%")

    query += " ORDER BY fecha DESC"

    conn = sqlite3.connect('inventario.db')
    cursor = conn.execute(query, params)
    registros = cursor.fetchall()
    conn.close()

    return render_template('auditoria.html', registros=registros)

# 📥 Exportar auditoría como CSV con firma digital
@app.route('/auditoria/exportar')
@login_required
def exportar_auditoria():
    if not es_admin(session['usuario']):
        return "Acceso restringido", 403

    conn = sqlite3.connect('inventario.db')
    cursor = conn.execute("SELECT fecha, archivo, destino FROM auditoria_envios ORDER BY fecha DESC")
    registros = cursor.fetchall()
    conn.close()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Fecha', 'Archivo', 'Destino'])
    writer.writerows(registros)

    contenido = output.getvalue()
    hash_csv = hashlib.sha256(contenido.encode()).hexdigest()
    contenido += f"\n# SHA256: {hash_csv}"

    response = Response(contenido, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=auditoria_backups.csv'
    return response

# 📄 Exportar auditoría como PDF
@app.route('/auditoria/pdf')
@login_required
def exportar_pdf():
    if not es_admin(session['usuario']):
        return "Acceso restringido", 403

    path = generar_pdf()
    return send_file(path, as_attachment=True)

# 🚀 Ejecutar app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
