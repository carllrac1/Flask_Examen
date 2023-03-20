from flask import Blueprint, render_template
from flask_security import login_required
from flask_security.decorators import roles_required, roles_accepted
from flask_login import login_required, current_user
from sqlalchemy import func

from project.models import Producto

from . import db

main = Blueprint('main', __name__)

#Definimos la ruta para la pagina principal

@main.route('/')
def index():
    productos = db.session.query(Producto).order_by(func.random()).limit(3)
    return render_template('index.html', productos=productos)

#Definimos la ruta para la pagina de perfil

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/formulario')
def formulario():
    return render_template('formulario.html')