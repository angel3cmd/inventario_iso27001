from flask import Blueprint, request, redirect, render_template, session
from auth import login_required
from utils.render import render_con_idioma
from db import get_db

activos_blueprint = Blueprint('activos', __name__)

@activos_blueprint.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar_activo():
    if request.method == 'POST':
        datos = {k: request.form.get(k) for k in [
            'nombre', 'tipo', 'propietario', 'ubicacion',
            'clasificacion', 'estado', 'fecha_alta', 'etiqueta'
        ]}
        db = get_db()
        db.execute("""
            INSERT INTO activos (nombre, tipo, propietario, ubicacion, clasificacion, estado, fecha_alta, etiqueta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(datos.values()))
        db.commit()
        return redirect('/dashboard')
    return render_con_idioma('agregar_activo.html')


@activos_blueprint.route('/agregar_relacion', methods=['GET', 'POST'])
@login_required
def agregar_relacion():
    db = get_db()
    if request.method == 'POST':
        activo_id = request.form['activo_id']
        ci_relacionado_id = request.form['ci_relacionado_id']
        tipo_relacion = request.form['tipo_relacion']
        db.execute("""
            INSERT INTO relaciones_ci (activo_id, ci_relacionado_id, tipo_relacion)
            VALUES (?, ?, ?)
        """, (activo_id, ci_relacionado_id, tipo_relacion))
        db.commit()
        return redirect('/dashboard')

    activos = db.execute("SELECT id, nombre FROM activos").fetchall()
    cis = db.execute("SELECT id, nombre FROM activos").fetchall()  # o tabla separada si aplica
    return render_con_idioma('agregar_relacion.html', activos=activos, cis=cis)


@activos_blueprint.route('/validacion_iso')
@login_required
def validacion_iso():
    db = get_db()
    activos_con_error = db.execute("""
        SELECT * FROM activos
        WHERE clasificacion IS NULL OR clasificacion NOT IN ('Confidencial', 'Interno', 'Personal')
           OR etiqueta IS NULL
    """).fetchall()
    return render_con_idioma('validacion_iso.html', activos_con_error=activos_con_error)
