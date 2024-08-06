# routes/brands.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.Brand import Brand
from models.Product import Product
from utils.db import db

brands = Blueprint('brands', __name__)

def check_marca(name, ammount):
    if not isinstance(name, str) or not name.strip():
        flash('El nombre de la marca debe ser un string no vacío', 'error')
        return False
    try:
        ammount = int(ammount)
        if ammount < 1:
            flash('La cantidad de artículos debe ser mayor a 0', 'error')
            return False
    except ValueError:
        flash('La cantidad de artículos debe ser un número entero válido', 'error')
        return False
    return True



@brands.route('/', methods=['GET'])
def ver_marcas():
    
    brands = Brand.query.all()
    return render_template('brands.html', brands=brands)

@brands.route('/add-brand', methods=['GET', 'POST'])
def add_marca():
    if request.method == 'POST':
        namet = request.form['name']
        cant = request.form['ammount_art']
        if check_marca(namet, cant):
            nueva_marca = Brand(name=namet, ammount_art=cant)
            db.session.add(nueva_marca)
            db.session.commit()
            flash('Marcas agregada con exito')
            return redirect(url_for('brands.ver_marcas'))
    return render_template('add_marca.html')

@brands.route('/edit-marca/<int:id>', methods=['GET', 'POST'])
def edit_marca(id):
    marca = Brand.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        cant_art= request.form['cant_art']
        if check_marca(nombre,cant_art):
            marca.nombre = nombre
            marca.cant_art= int(cant_art)
            db.session.commit()
            flash('Marcas actualizada con exito')
            return redirect(url_for('brands.ver_marcas'))
    return render_template('edit_marca.html', marca=marca)

@brands.route('/delete-marca/<int:id>', methods=['GET'])
def delete_marca(id):
    marca = Brand.query.get_or_404(id)
    db.session.delete(marca)
    db.session.commit()
    flash('Marcas eliminada con exito')
    return redirect(url_for('brands.ver_marcas'))


@brands.route('/lista-de-productos/<string:marca_nombre>', methods=['GET'])
def listar_productos(marca_nombre):
    # Fetch the brand by name
    marcap = Brand.query.filter_by(nombre=marca_nombre).first_or_404()  # Use filter_by for name
    # Fetch products associated with the brand
    productosp = Product.query.filter_by(marca=marcap.nombre).all()  # Use the Marcas object to filter products
    return render_template('lista-de-productos.html', marca=marcap, productos=productosp)
