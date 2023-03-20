import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore


#Creamos una istancia de SQLAlchemy

db = SQLAlchemy()
from .models import User, Role

#Creamos un objeto de SQLAlchemyUserDatastore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

#Metodo de inicio de la aplicacion
def create_app():
    #Creamos nuestra aplicacion de Flask
    app = Flask(__name__)

    #Configuraciones necesarias
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/flaskexam'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = 'secretsalt'

    #template del login
    app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login.html'

    #url del login
    app.config['SECURITY_LOGIN_URL'] = '/login'

    db.init_app(app)
    #Metodo para crear la base de datos en la primera ejecucion

    @app.before_first_request
    def create_all():
        db.create_all()

    #Conectando los modelos de Flask-security usando SQLALCHEMYUSERDATASTORE
    security = Security(app, user_datastore)

    
    #Registramos dos blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .productos import productos as productos_blueprint
    app.register_blueprint(productos_blueprint)

    return app