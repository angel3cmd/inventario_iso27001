from flask import request, redirect, flash
from models_cmdb import agregar_relacion_ci, obtener_relaciones_ci
from utils.render import render_con_idioma
from auth import login_required

@app.route('/relaciones')
@login_required
def listar_relaciones():
    relaciones = obtener_relaciones_ci()
    return render_con_idioma('relaciones.html', relaciones=relaciones)

@app.route('/relaciones/agregar', methods=['POST'])
@login_required
def crear_relacion():
    datos = request.form
    agregar_relacion_ci(
        datos['origen_tipo'], int(datos['origen_id']),
        datos['destino_tipo'], int(datos['destino_id']),
        datos['tipo_relacion'], datos.get('descripcion', '')
    )
    flash('Relación creada correctamente', 'success')
    return redirect('/relaciones')
