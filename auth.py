from flask import session, redirect

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def autenticar(usuario, clave):
    import sqlite3
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario=? AND clave=?', (usuario, clave))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def es_admin(usuario):
    return usuario == 'admin'  # o consulta en base de datos

# Simulación de usuarios con roles
USUARIOS = {
    'admin': {'clave': 'admin123', 'rol': 'admin'},
    'auditor': {'clave': 'auditor123', 'rol': 'auditor'},
    'operador': {'clave': 'operador123', 'rol': 'operador'}
}

def autenticar(usuario, clave):
    return usuario in USUARIOS and USUARIOS[usuario]['clave'] == clave

def obtener_rol(usuario):
    return USUARIOS.get(usuario, {}).get('rol')

def es_admin(usuario):
    return obtener_rol(usuario) == 'admin'

def es_auditor(usuario):
    return obtener_rol(usuario) == 'auditor'

def es_operador(usuario):
    return obtener_rol(usuario) == 'operador'

def login_required(f):
    from functools import wraps
    from flask import session, redirect
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function