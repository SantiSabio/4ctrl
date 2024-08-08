from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from models.Product import Product
from models.Brand import Brand
from app import db

products = Blueprint('products', __name__)


@products.route('/')
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)


@products.route('/get_brands', methods=['GET'])
def get_brands():
    query = request.args.get('q', '')
    brands = Brand.query.filter(Brand.nombre.ilike(f'%{query}%')).all()
    return jsonify([{'nombre': brand.nombre} for brand in brands])

def check(name, brand, price):
    if not isinstance(name, str) or not name.strip():
        flash('El nombre debe ser un string no vacío')
        return False

    if not isinstance(brand, str) or not brand.strip():
        flash('La marca debe ser un string no vacío')
        return False

    try:
        price = float(price)
        if price <= 0:
            flash('El precio debe ser un número positivo')
            return False
    except ValueError:
        flash('El precio debe ser un número válido')
        return False

    return True

@products.route('/add_products', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        price = request.form['price']

        brand_exists = Brand.query.filter_by(name=brand).first()
        if not brand_exists:
            flash('La marca seleccionada no existe')
            return redirect(url_for('products.add_product'))

        if check(name, brand, price):
            new_product = Product(name=name, brand=brand, price=float(price))
            db.session.add(new_product)
            db.session.commit()
            flash('Producto agregado con éxito')
            return redirect(url_for('products.home'))
        else:
            brands = Brand.query.all()
            return render_template('index.html', nombre=name, marca=brand, precio=price, marcas=brands)

    brands = Brand.query.all()
    return render_template('index.html', marcas=brands)

@products.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        price = request.form['price']

        brand_exists = Brand.query.filter_by(name=brand).first()
        if not brand_exists:
            flash('La marca seleccionada no existe')
            return redirect(url_for('products.edit_product', id=id))

        if check(name, brand, price):
            product.name = name
            product.brand = brand
            product.price = float(price)
            db.session.commit()
            flash('Producto actualizado con éxito')
            return redirect(url_for('products.home'))
        else:
            return render_template('edit_product.html', product=product, nombre=name, marca=brand, precio=price)

    return render_template('edit_product.html', product=product)

@products.route('/delete/<int:id>', methods=['GET'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado con éxito')
    return redirect(url_for('products.home'))
