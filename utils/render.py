# utils/render.py
from flask import render_template, session
from lang import traducciones

def render_con_idioma(template, **kwargs):
    idioma = session.get('idioma', 'es')
    t = traducciones.get(idioma, traducciones['es'])
    return render_template(template, t=t, **kwargs)
