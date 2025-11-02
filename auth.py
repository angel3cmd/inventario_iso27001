from flask import Blueprint, render_template, request, redirect, session, flash
from functools import wraps
from db import get_db
from lang import traducciones

auth_blueprint = Blueprint('auth', __name__)

# 🧠 Usuarios simulados (solo para pruebas)
USUARIOS = {
    'admin': {
        'id': 1,
        'nombre': 'Administrador General',
        'clave': 'admin123',
        'rol': 'admin'
    },
    'auditor': {
        'id': 2,
        'nombre': 'Auditor de Seguridad',
        'clave': 'auditor123',
        'rol': 'auditor'
    },
    'operador': {
        'id': 3,
        'nombre': 'Operador Técnico',
        'clave': 'operador123',
        'rol': 'operador'
    }
}

# 🔍 Autenticación
def autenticar(usuario, clave):
    if usuario in USUARIOS and USUARIOS[usuario]['clave'] == clave:
        return {
            'id': USUARIOS[usuario]['id'],
            'usuario': usuario,
            'nombre': USUARIOS[usuario]['nombre'],
            'rol': USUARIOS[usuario]['rol']
        }
    return None

# 🎭 Roles
def obtener_rol(usuario):
    return USUARIOS.get(usuario, {}).get('rol')

def es_admin(usuario):
    return obtener_rol(usuario) == 'admin'

def es_auditor(usuario):
    return obtener_rol(usuario) == 'auditor'

def es_operador(usuario):
    return obtener_rol(usuario) == 'operador'

# 🔒 Decorador para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# 🔐 Ruta de login
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    idioma = session.get('idioma', 'es')
    if request.method == 'POST':
        usuario_input = request.form['usuario']
        clave = request.form['clave']
        usuario_obj = autenticar(usuario_input, clave)
        if usuario_obj:
            session['usuario'] = usuario_obj['usuario']
            session['usuario_id'] = usuario_obj['id']
            session['usuario_nombre'] = usuario_obj['nombre']
            session['rol'] = usuario_obj['rol']
            return redirect('/')
        else:
            flash("Credenciales incorrectas", "danger")
    return render_template('login.html', t=traducciones[idioma])

# 🔓 Ruta de logout
@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# 📝 Registro de nuevos usuarios (base de datos)
@auth_blueprint.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    idioma = session.get('idioma', 'es')
    if request.method == 'POST':
        usuario = request.form['usuario']
        nombre = request.form['nombre']
        clave = request.form['clave']
        rol = request.form.get('rol', 'operador')

        db = get_db()
        try:
            db.execute("""
                INSERT INTO usuarios (usuario, nombre, clave, rol)
                VALUES (?, ?, ?, ?)
            """, (usuario, nombre, clave, rol))
            db.commit()
            flash("Usuario registrado exitosamente", "success")
            return redirect('/login')
        except Exception as e:
            flash("Error al registrar usuario: " + str(e), "danger")

    return render_template('registrar_usuario.html', t=traducciones[idioma])
