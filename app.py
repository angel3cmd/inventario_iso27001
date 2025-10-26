import os
import csv
import hashlib
import sqlite3
from io import StringIO
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, send_file, Response
from flasgger import Swagger, swag_from
from models import init_db
from controllers.activos_controller import agregar_activo, obtener_activos
from auth import login_required, autenticar, es_admin, obtener_rol, auth_blueprint
from dashboard import obtener_metricas, dashboard_blueprint
from export import exportar_excel
from decrypt_file import decrypt_file
from generar_pdf_auditoria import generar_pdf
from config import config_by_name
from flask import request, jsonify
from controllers.activos_controller import buscar_activos
from flask import flash, redirect, url_for
from datetime import datetime
from lang import traducciones
from utils.render import render_con_idioma

# 🗂️ Crear carpetas persistentes si no existen
os.makedirs('data', exist_ok=True)
os.makedirs('backups', exist_ok=True)

# 🔧 Configuración inicial
load_dotenv()
#app = Flask(__name__)
#Para que agregue todo desde base
app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "clave-segura")  # ← Asegúrate de tener esto
app.config.from_object(config_by_name[os.getenv('FLASK_ENV', 'development')])
swagger = Swagger(app)

# 🔌 Registrar blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(dashboard_blueprint)

# 🗃️ Inicializar base de datos
init_db()

# 🔐 Crear tabla auditoria_envios si no existe
conn = sqlite3.connect('data/inventario.db')
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

# 🔐 Proteger Swagger UI y JSON
@app.before_request
def proteger_swagger():
    idioma = session.get('idioma', 'es')
    if request.path.startswith('/apidocs') or request.path.startswith('/apispec_1.json'):
        if 'usuario' not in session:
            return redirect('/login')

@app.route('/home')
@login_required
def home():
    rol = session.get('rol', 'usuario')
    return render_con_idioma('home.html', rol=rol)

@app.route('/login', methods=['GET', 'POST'])
@swag_from('swagger/login.yaml')
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if autenticar(usuario, clave):
            session['usuario'] = usuario
            session['rol'] = obtener_rol(usuario)
            return redirect('/home')
    return render_con_idioma('login.html')

@app.route('/logout')
def logout():
    idioma = session.get('idioma', 'es')
    t = traducciones.get(idioma, traducciones['es'])  # fallback por si falta el idioma
    session.clear()
    return redirect('/login')

@app.route('/')
@login_required
def index():
    metricas = obtener_metricas()
    return render_con_idioma('index.html', metricas=metricas, year=datetime.now().year)

#@app.route('/')
#@login_required
#def index():
#    activos = obtener_activos()
#    year = datetime.now().year
#    return render_template('index.html', activos=activos, year=year)

@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    try:
        agregar_activo(
            nombre=request.form['nombre'],
            tipo=request.form['tipo'],
            propietario=request.form['propietario'],
            ubicacion=request.form['ubicacion'],
            clasificacion=request.form['clasificacion'],
            estado=request.form['estado'],
            fecha_alta=request.form['fecha_alta'],
            etiqueta=request.form.get('etiqueta', '')
        )
        flash("Activo guardado exitosamente", "success")
        return redirect('/')
    except ValueError as e:
        return render_con_idioma('error.html', mensaje=str(e)), 400

@app.route('/dashboard')
@login_required
@swag_from('swagger/dashboard.yaml')
def dashboard():
    metricas = obtener_metricas()  # ← esta función debe existir y devolver un dict
    activos = obtener_activos()
    return render_con_idioma('dashboard.html', metricas=metricas, year=datetime.now().year)


@app.route('/exportar', methods=['GET', 'POST'])
@login_required
@swag_from('swagger/exportar_excel.yaml')
def exportar():
    archivo_generado = None
    if request.method == 'POST':
        archivo_generado = exportar_excel()
        flash("Exportación completada exitosamente", "success")
    return render_con_idioma('exportar.html', archivo_generado=archivo_generado)

@app.route('/restaurar')
@login_required
@swag_from('swagger/restaurar.yaml')
def listar_backups():
    archivos = [f for f in os.listdir('backups') if f.endswith('.enc')]
    return render_con_idioma('restaurar.html', archivos=archivos)

@app.route('/restaurar/<nombre>')
@login_required
@swag_from('swagger/restaurar.yaml')
def restaurar(nombre):
    encrypted_path = os.path.join('backups', nombre)
    output_path = os.path.join('backups', 'restaurado_' + nombre.replace('.enc', '.xlsx'))

    if not os.path.exists(encrypted_path):
        return "Archivo no encontrado", 404

    decrypt_file(encrypted_path, output_path)

    conn = sqlite3.connect('data/inventario.db')
    conn.execute("INSERT INTO auditoria_envios (fecha, archivo, destino) VALUES (?, ?, ?)",
                 (datetime.now().isoformat(), os.path.basename(output_path), 'restauración local'))
    conn.commit()
    conn.close()

    return send_file(output_path, as_attachment=True)

@app.route('/auditoria', methods=['GET', 'POST'])
@login_required
@swag_from('swagger/auditoria.yaml')
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

    conn = sqlite3.connect('data/inventario.db')
    cursor = conn.execute(query, params)
    registros = cursor.fetchall()
    conn.close()

    return render_con_idioma('auditoria.html', registros=registros)

@app.route('/auditoria/exportar')
@login_required
@swag_from('swagger/auditoria.yaml')
def exportar_auditoria():
    if not es_admin(session['usuario']):
        return "Acceso restringido", 403

    conn = sqlite3.connect('data/inventario.db')
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

@app.route('/auditoria/pdf')
@login_required
@swag_from('swagger/auditoria.yaml')
def exportar_pdf():
    if not es_admin(session['usuario']):
        return "Acceso restringido", 403

    path = generar_pdf()
    return send_file(path, as_attachment=True)

#@app.route('/ping', methods=['GET'])
#def ping():
#    idioma = session.get('idioma', 'es')
#    return "Pong!", 200

#Búsqueda en tiempo real
@app.route("/buscar_activos")
def buscar_activos_route():
    query = request.args.get("query", "")
    resultados = buscar_activos(query)
    return jsonify([
        {
            "nombre": r[0],
            "etiqueta": r[1],
            "propietario": r[2]
        } for r in resultados
    ])

#Importar fecha a las vistas

@app.context_processor
def inject_year():
    from datetime import datetime
    return {'year': datetime.now().year}

#Obtener Metricas
def obtener_metricas():
    conn = sqlite3.connect('data/inventario.db')
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM activos").fetchone()[0]
    confidenciales = cursor.execute("SELECT COUNT(*) FROM activos WHERE clasificacion = 'Confidencial'").fetchone()[0]
    inactivos = cursor.execute("SELECT COUNT(*) FROM activos WHERE estado = 'Inactivo'").fetchone()[0]

    conn.close()
    return {
        "Total de activos": total,
        "Confidenciales": confidenciales,
        "Inactivos": inactivos
    }
    
#complemento para el cambio de idioma
@app.route('/idioma/<lang>')
def cambiar_idioma(lang):
    if lang in ['es', 'en']:
        session['idioma'] = lang
    return redirect(request.referrer or '/home')
 
#Idioma por defecto
@app.before_request
def establecer_idioma_por_defecto():
    if 'idioma' not in session:
        session['idioma'] = 'es'

#Centralizador de inidioma
def render_con_idioma(template, **kwargs):
    idioma = session.get('idioma', 'es')
    t = traducciones.get(idioma, traducciones['es'])
    return render_template(template, t=t, **kwargs)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
