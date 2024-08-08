# routes/brands.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.Brand import Brands
from models.Product import Products
from app import db

brands = Blueprint('brands', __name__)


def check_brand(name):
    if not isinstance(name, str) or not name.strip():
        flash('El nombre de la marca debe ser un string no vacío', 'error')
        return False
    return True

@brands.route('/', methods=['GET'])
def home():
    brands = Brands.query.all()
    return render_template('brands.html', brands=brands)

@brands.route('/add-brand', methods=['GET', 'POST'])
def add_brand():
    if request.method == 'POST':
        name = request.form['name']
        amount = 0
        if check_brand(name):
            new_brand = Brands(name=name)
            db.session.add(new_brand)
            db.session.commit()
            flash('Marcas agregada con éxito')
            return redirect(url_for('brands.home'))
    return render_template('add_brand.html')

@brands.route('/delete-brand/<int:id>', methods=['GET'])
def delete_brand(id):
    brand = Brands.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    flash('Marcas eliminada con éxito')
    return redirect(url_for('brands.home'))

@brands.route('/products-list/<string:brand_name>', methods=['GET'])
def list_products(brand_name):
    brand = Brands.query.filter_by(name=brand_name).first_or_404()
    products = Products.query.filter_by(brand=brand.name).all()
    return render_template('product_list.html', brand=brand, products=products)
