from flask import Blueprint, render_template, session
from utils.render import render_con_idioma
from auth import login_required
from db import get_db
#Se cambia esta ruta
#from models import obtener_activos # asegúrate de importar esta función
from controllers.activos_controller import obtener_activos # asegúrate de importar esta función
dashboard_blueprint = Blueprint('dashboard', __name__)


import sqlite3

@dashboard_blueprint.route('/dashboard')
@login_required
def dashboard():
    metricas = obtener_metricas()
    activos = obtener_activos()
    return render_con_idioma('dashboard.html', metricas=metricas, activos=activos)

def obtener_metricas():
    db = get_db()
    return {
        "Total de activos": db.execute("SELECT COUNT(*) FROM activos").fetchone()[0],
        "Total de integraciones": db.execute("SELECT COUNT(*) FROM integraciones").fetchone()[0],
        "Total de relaciones": db.execute("SELECT COUNT(*) FROM relaciones_ci").fetchone()[0],
        "Errores ISO 27001": db.execute("""
            SELECT COUNT(*) FROM activos
            WHERE clasificacion IS NULL OR clasificacion NOT IN ('Confidencial', 'Interno', 'Personal')
               OR etiqueta IS NULL
        """).fetchone()[0]
    }


__all__ = ['obtener_metricas', 'dashboard_blueprint']
