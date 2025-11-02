from flask import Blueprint, request, redirect, flash
from models_cmdb import agregar_activo, obtener_activos, buscar_activos
from utils.render import render_con_idioma
from auth import login_required
from flask import blueprints

activos_blueprint = Blueprint('activos', __name__)

@activos_blueprint.route('/activos')

@login_required
def listar_activos():
    activos = obtener_activos()
    return render_con_idioma('activos.html', activos=activos)

@activos_blueprint.route('/activos/agregar', methods=['POST'])
@login_required
def crear_activo():
    try:
        datos = request.form
        agregar_activo(
            datos['nombre'], datos['tipo'], datos['propietario'],
            datos['ubicacion'], datos['clasificacion'], datos['estado'],
            datos['fecha_alta'], datos.get('etiqueta', '')
        )
        flash('Activo agregado correctamente', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect('/activos')

@activos_blueprint.route('/activos/buscar')
@login_required
def buscar():
    criterio = request.args.get('q', '')
    resultados = buscar_activos(criterio)
    return render_con_idioma('activos.html', activos=resultados)
