import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, redirect, session
from models import init_db, agregar_activo, obtener_activos
from auth import login_required, autenticar
from dashboard import obtener_metricas
from export import exportar_excel

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_por_defecto')
init_db()

@app.route('/')
@login_required
def index():
    activos = obtener_activos()
    return render_template('index.html', activos=activos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if autenticar(request.form['usuario'], request.form['clave']):
            session['usuario'] = request.form['usuario']
            return redirect('/')
    return render_template('login.html')

@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    agregar_activo(**request.form)
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    metricas = obtener_metricas()
    return render_template('dashboard.html', metricas=metricas)

@app.route('/exportar')
@login_required
def exportar():
    exportar_excel()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
