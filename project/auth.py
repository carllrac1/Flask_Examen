from flask_login import login_required, current_user, login_user, logout_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password
from .models import User
from . import db
from . import user_datastore

auth = Blueprint('auth', __name__, url_prefix='/security')


#if there is a user logged in, redirect to the home page
@auth.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Consultamos si existe un usuario con el email ingresado
    user = User.query.filter_by(email=email).first()

    #Verificamos si el usuario existe y si la contraseña es correcta
    if not user or not check_password_hash(user.password, password):
        flash('Revisa tus credenciales e intenta de nuevo.')
        return redirect(url_for('auth.login')) #Redireccionamos a la pagina de login

    # Si llegamos a este punto, el usuario existe y la contraseña es correcta y creamos la sesion
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/register', methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    #Verificamos si el usuario ya existe
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    #Creamos un nuevo usuario
    user_datastore.create_user(name = name, email = email, password = generate_password_hash(password, method='sha256'))

    #Agregamos el usuario a la base de datos
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    #Cerramos la sesion
    logout_user()
    return redirect(url_for('main.index'))

