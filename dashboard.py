from flask import Blueprint, render_template, session
from auth import login_required
dashboard_blueprint = Blueprint('dashboard', __name__)


import sqlite3


def obtener_metricas():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM activos")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM activos WHERE clasificacion='Confidencial'")
    confidencial = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM activos WHERE propietario IS NULL OR propietario=''")
    sin_propietario = cursor.fetchone()[0]
    conn.close()
    return {
        "total": total,
        "confidencial": confidencial,
        "sin_propietario": sin_propietario
    }


@dashboard_blueprint.route('/dashboard')
@login_required
def dashboard():
    metricas = obtener_metricas()
    return render_template('dashboard.html', metricas=metricas)


__all__ = ['obtener_metricas', 'dashboard_blueprint']
