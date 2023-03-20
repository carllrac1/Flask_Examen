#Importamos el objeto de la base de datos __init__.py
from . import db
from flask_sqlalchemy import SQLAlchemy
#Importamos la clase UserMixin de  flask_login
from flask_security import UserMixin, RoleMixin


user_roles = db.Table('user_roles',
  db.Column('userId', db.Integer, db.ForeignKey('user.id')),
  db.Column('roleId', db.Integer, db.ForeignKey('role.id')),
)

class User(UserMixin, db.Model):
    """User account model."""
    
    _tablename_ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role',
        secondary=user_roles,
        backref = db.backref('users', lazy='dynamic')
    )

class Role(RoleMixin, db.Model):
    """Role model"""
    _tablename_ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

class Producto(db.Model):
    """Producto model"""
    _tablename_ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    artista = db.Column(db.String(100), nullable=False)
    annio = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(255))