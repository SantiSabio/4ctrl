# routes/marcas.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.tables import Marcas
from utils.db import db

marcas = Blueprint('marcas', __name__)

def check_marca(nombre, cantidad):
    if not isinstance(nombre, str) or not nombre.strip():
        flash('El nombre de la marca debe ser un string no vacío', 'error')
        return False
    try:
        cantidad = int(cantidad)
        if cantidad < 1:
            flash('La cantidad de artículos debe ser mayor a 0', 'error')
            return False
    except ValueError:
        flash('La cantidad de artículos debe ser un número entero válido', 'error')
        return False
    return True



@marcas.route('/', methods=['GET'])
def ver_marcas():
    
    marcas = Marcas.query.all()
    return render_template('marcas.html', marcas=marcas)

@marcas.route('/add-marca', methods=['GET', 'POST'])
def add_marca():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cant = request.form['cant_art']
        if check_marca(nombre, cant):
            nueva_marca = Marcas(nombre=nombre, cant_art=cant)
            db.session.add(nueva_marca)
            db.session.commit()
            flash('Marcas agregada con exito')
            return redirect(url_for('marcas.ver_marcas'))
    return render_template('add_marca.html')

@marcas.route('/edit-marca/<int:id>', methods=['GET', 'POST'])
def edit_marca(id):
    marca = Marcas.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        cant_art= request.form['cant_art']
        if check_marca(nombre,cant_art):
            marca.nombre = nombre
            marca.cant_art= int(cant_art)
            db.session.commit()
            flash('Marcas actualizada con exito')
            return redirect(url_for('marcas.ver_marcas'))
    return render_template('edit_marca.html', marca=marca)

@marcas.route('/delete-marca/<int:id>', methods=['GET'])
def delete_marca(id):
    marca = Marcas.query.get_or_404(id)
    db.session.delete(marca)
    db.session.commit()
    flash('Marcas eliminada con exito')
    return redirect(url_for('marcas.ver_marcas'))
