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
