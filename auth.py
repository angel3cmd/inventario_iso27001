from flask import Blueprint, render_template, request, redirect, session
from functools import wraps
import sqlite3

auth_blueprint = Blueprint('auth', __name__)

# 🔐 Ruta de login
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if autenticar(usuario, clave):
            session['usuario'] = usuario
            session['rol'] = obtener_rol(usuario)
            return redirect('/home')
    return render_template('login.html')

# 🔒 Decorador para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# 🧠 Simulación de usuarios con roles
USUARIOS = {
    'admin': {'clave': 'admin123', 'rol': 'admin'},
    'auditor': {'clave': 'auditor123', 'rol': 'auditor'},
    'operador': {'clave': 'operador123', 'rol': 'operador'}
}

# 🔍 Autenticación
def autenticar(usuario, clave):
    return usuario in USUARIOS and USUARIOS[usuario]['clave'] == clave

# 🎭 Roles
def obtener_rol(usuario):
    return USUARIOS.get(usuario, {}).get('rol')

def es_admin(usuario):
    return obtener_rol(usuario) == 'admin'

def es_auditor(usuario):
    return obtener_rol(usuario) == 'auditor'

def es_operador(usuario):
    return obtener_rol(usuario) == 'operador'
