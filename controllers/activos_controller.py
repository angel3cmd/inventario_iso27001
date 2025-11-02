from flask import Blueprint, request, redirect, flash
from models_cmdb import agregar_activo as guardar_activo, obtener_activos, buscar_activos
from utils.render import render_con_idioma
from auth import login_required
from db import get_db
from datetime import datetime
from models_cmdb import (
    asignar_activo_a_usuario,
    liberar_activo,
    obtener_activos_disponibles,
    obtener_activos_asignados_a_usuario,
    obtener_historial_asignaciones_activo
)

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

@activos_blueprint.route('/asignar_activo', methods=['GET', 'POST'])
@login_required
def asignar_activo():
    db = get_db()
    if request.method == 'POST':
        try:
            activo_id = request.form['activo_id']
            usuario_id = request.form['usuario_id']
            fecha_asignacion = request.form['fecha_asignacion']
            observaciones = request.form.get('observaciones', '')
            asignar_activo_a_usuario(activo_id, usuario_id, fecha_asignacion, observaciones)
            flash("Activo asignado correctamente", "success")
            return redirect('/dashboard')
        except ValueError as e:
            flash(str(e), "danger")

    activos = obtener_activos_disponibles()
    usuarios = db.execute("SELECT id, nombre FROM usuarios").fetchall()
    return render_con_idioma('asignar_activo.html', activos=activos, usuarios=usuarios)

@activos_blueprint.route('/usuario/<int:usuario_id>/activos')
@login_required
def activos_asignados(usuario_id):
    activos = obtener_activos_asignados_a_usuario(usuario_id)
    usuario = get_db().execute("SELECT nombre FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    return render_con_idioma('activos_asignados.html', activos=activos, usuario=usuario)

@activos_blueprint.route('/liberar_activo/<int:activo_id>', methods=['POST'])
@login_required
def liberar_activo_view(activo_id):
    try:
        fecha_liberacion = datetime.now().strftime('%Y-%m-%d')
        liberar_activo(activo_id, fecha_liberacion)
        flash("Activo liberado correctamente", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect('/dashboard')  # o a donde prefieras redirigir
