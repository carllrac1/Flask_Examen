import time
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security import login_required
from flask_security.decorators import roles_required, roles_accepted
from flask_login import login_required, current_user

from .models import Producto

from . import db

import os 

productos = Blueprint('productos', __name__)

@productos.route('/dashboard/productos')
@login_required
@roles_required('admin')
def dashboard_productos():
    productos = db.session.query(Producto).order_by(Producto.annio.asc()).all()
    return render_template('productos/dashboard.html', productos=productos)

@productos.route('/productos/crear', methods=['POST'])
@login_required
@roles_required('admin')
def crear_producto():
    nombre = request.form['nombre']
    artista = request.form['artista']
    annio = request.form['annio']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.files['imagen']

    #if in static theres no folder media so we need to create one
    if not os.path.exists('project/static/media'):
        os.makedirs('project/static/media')

    #salvamos la imagen con un nombre aleatorio considerando la fecha y la hora
    imagen_nombre = str(int(time.time())) + '.' + imagen.filename.rsplit('.', 1)[1]
    imagen.save(os.path.join('project/static/media', imagen_nombre))
    producto = Producto(nombre=nombre, artista=artista ,annio=annio, precio=precio, cantidad=cantidad, imagen=imagen_nombre)
    
    db.session.add(producto)
    db.session.commit()
    flash('Producto creado correctamente')
    return redirect(url_for('productos.dashboard_productos'))

@productos.route('/productos/editar/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    nombre = request.form['nombre']
    annio = request.form['annio']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    artista = request.form['artista']
    if request.files['imagen'].filename != '':
        imagen = request.files['imagen']
        if not os.path.exists('project/static/media'):
            os.makedirs('project/static/media')
        imagen_nombre = str(int(time.time())) + '.' + imagen.filename.rsplit('.', 1)[1]
        imagen.save(os.path.join('project/static/media', imagen_nombre))
        producto.imagen = imagen_nombre

    producto.nombre = nombre
    producto.annio = annio
    producto.precio = precio
    producto.cantidad = cantidad
    producto.artista = artista
    db.session.commit()
    flash('Producto editado correctamente')
    return redirect(url_for('productos.dashboard_productos'))

@productos.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('productos.dashboard_productos'))


@productos.route('/productos/catalogo')
@login_required
@roles_required('cliente')
def catalogo_productos():
    productos = db.session.query(Producto).all()
    return render_template('productos/catalogo.html', productos=productos)

