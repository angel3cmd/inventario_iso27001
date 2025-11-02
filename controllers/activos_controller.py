from flask import Blueprint, request, redirect, flash
from models_cmdb import agregar_activo as guardar_activo, obtener_activos, buscar_activos
from utils.render import render_con_idioma
from auth import login_required
from db import get_db

activos_blueprint = Blueprint('activos', __name__)

@activos_blueprint.route('/activos')
@login_required
def listar_activos():
    activos = obtener_activos()
    return render_con_idioma('activos.html', activos=activos)

@activos_blueprint.route('/activos/agregar', methods=['POST'])
@login_required
def crear_activo():
    datos = request.form
    try:
        guardar_activo(
            datos['nombre'], datos['tipo'], datos['propietario'],
            datos['ubicacion'], datos['clasificacion'], datos['estado'],
            datos['fecha_alta'], datos.get('etiqueta', '')
        )
        flash("Activo guardado exitosamente", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect('/activos')

@activos_blueprint.route('/activos/buscar')
@login_required
def buscar():
    criterio = request.args.get('q', '')
    resultados = buscar_activos(criterio)
    return render_con_idioma('activos.html', activos=resultados)
@activos_blueprint.route('/activos/validacion_iso')
@login_required
def validacion_iso():
    return render_con_idioma('validacion_iso.html')
@activos_blueprint.route('/activos/generar_reporte_iso')
@login_required
def generar_reporte_iso():
    return render_con_idioma('generar_reporte_iso.html')
@activos_blueprint.route('/activos/auditoria_nueva')
@login_required
def auditoria_nueva():
    return render_con_idioma('auditoria_nueva.html')        

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
    cis = db.execute("SELECT id, nombre FROM activos").fetchall()
    return render_con_idioma('agregar_relacion.html', activos=activos, cis=cis)
