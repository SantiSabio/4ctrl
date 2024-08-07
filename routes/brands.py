# routes/brands.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.Brand import Brands
from models.Product import Products
from app import db

brands = Blueprint('brands', __name__)


@brands.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = 'administrador'
        if request.form.get('password') == password:
            return redirect(url_for('brands.home'))
        else:
            return render_template("login.html", error='Contraseña incorrecta')
    return render_template("login.html")

@brands.route('/home')
def home():
    brands = Brands.query.all()
    return render_template("brands.html", brands=brands)

def check_brand(name, amount):
    if not isinstance(name, str) or not name.strip():
        flash('El nombre de la marca debe ser un string no vacío', 'error')
        return False
    try:
        amount = int(amount)
        if amount < 1:
            flash('La cantidad de artículos debe ser mayor a 0', 'error')
            return False
    except ValueError:
        flash('La cantidad de artículos debe ser un número entero válido', 'error')
        return False
    return True

@brands.route('/', methods=['GET'])
def list_brands():
    brands = Brands.query.all()
    return render_template('brands.html', brands=brands)

@brands.route('/add-brand', methods=['GET', 'POST'])
def add_brand():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount_art']
        if check_brand(name, amount):
            new_brand = Brands(name=name, amount_art=amount)
            db.session.add(new_brand)
            db.session.commit()
            flash('Marcas agregada con éxito')
            return redirect(url_for('brands.list_brands'))
    return render_template('add_brand.html')

@brands.route('/edit-brand/<int:id>', methods=['GET', 'POST'])
def edit_brand(id):
    brand = Brands.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name']
        amount_art = request.form['amount_art']
        if check_brand(name, amount_art):
            brand.name = name
            brand.amount_art = int(amount_art)
            db.session.commit()
            flash('Marcas actualizada con éxito')
            return redirect(url_for('brands.list_brands'))
    return render_template('edit_brand.html', brand=brand)

@brands.route('/delete-brand/<int:id>', methods=['GET'])
def delete_brand(id):
    brand = Brands.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    flash('Marcas eliminada con éxito')
    return redirect(url_for('brands.list_brands'))

@brands.route('/products-list/<string:brand_name>', methods=['GET'])
def list_products(brand_name):
    brand = Brands.query.filter_by(name=brand_name).first_or_404()
    products = Products.query.filter_by(brand=brand.name).all()
    return render_template('products_list.html', brand=brand, products=products)
