# routes/brands.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.Brand import Brand
from models.Product import Product
from app import db

brands = Blueprint('brands', __name__)


# @brands.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         password = 'administrador'
#         if request.form.get('password') == password:
#             return redirect(url_for('brands.home'))
#         else:
#             return render_template("login.html", error='Contraseña incorrecta')
#     return render_template("login.html")

<<<<<<< HEAD
def check_brand(name):
=======
@brands.route('/')
def home():
    brands = Brand.query.all()
    return render_template("brands.html", brands=brands)

def check_brand(name, amount):
>>>>>>> 4e8e448b38ed7c8cc221ce907bb9cae4d2bfec11
    if not isinstance(name, str) or not name.strip():
        flash('El nombre de la marca debe ser un string no vacío', 'error')
        return False
    return True

@brands.route('/', methods=['GET'])
<<<<<<< HEAD
def home():
    brands = Brands.query.all()
=======
def list_brands():
    brands = Brand.query.all()
>>>>>>> 4e8e448b38ed7c8cc221ce907bb9cae4d2bfec11
    return render_template('brands.html', brands=brands)

@brands.route('/add-brand', methods=['GET', 'POST'])
def add_brand():
    if request.method == 'POST':
        name = request.form['name']
<<<<<<< HEAD
        amount = 0
        if check_brand(name):
            new_brand = Brands(name=name)
=======
        amount = request.form['amount_art']
        if check_brand(name, amount):
            new_brand = Brand(name=name, amount_art=amount)
>>>>>>> 4e8e448b38ed7c8cc221ce907bb9cae4d2bfec11
            db.session.add(new_brand)
            db.session.commit()
            flash('Marcas agregada con éxito')
            return redirect(url_for('brands.home'))
    return render_template('add_brand.html')

<<<<<<< HEAD
#@brands.route('/edit-brand/<int:id>', methods=['GET', 'POST'])
#def edit_brand(id):
#    brand = Brands.query.get_or_404(id)
#    if request.method == 'POST':
#        name = request.form['name']
#        amount_art = request.form['amount_art']
#            brand.name = name
#            brand.amount_art = int(amount_art)
#            db.session.commit()
#            flash('Marcas actualizada con éxito')
#            return redirect(url_for('brands.home'))
#    return render_template('edit_brand.html', brand=brand)
=======
@brands.route('/edit-brand/<int:id>', methods=['GET', 'POST'])
def edit_brand(id):
    brand = Brand.query.get_or_404(id)
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
>>>>>>> 4e8e448b38ed7c8cc221ce907bb9cae4d2bfec11

@brands.route('/delete-brand/<int:id>', methods=['GET'])
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    flash('Marcas eliminada con éxito')
    return redirect(url_for('brands.home'))

@brands.route('/products-list/<string:brand_name>', methods=['GET'])
def list_products(brand_name):
    brand = Brand.query.filter_by(name=brand_name).first_or_404()
    products = Product.query.filter_by(brand=brand.name).all()
    return render_template('product_list.html', brand=brand, products=products)
