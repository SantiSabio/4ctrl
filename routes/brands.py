# routes/brands.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.Brand import Brands
from models.Product import Products
from app import db

brands = Blueprint('brands', __name__)


#Chequea si el tipo de dato es correcto para la posterior anexion a base de datos (DontRepeatYourself)
def check_brand(name):
    if not isinstance(name, str) or not name.strip():
        flash('El nombre de la marca debe ser un string no vacío', 'error')
        return False
    return True

@brands.route('/', methods=['GET']) #Despliegue del home de brands
@login_required
def home():
    brands = Brands.query.all()
    return render_template('brands.html', brands=brands)

@brands.route('/add-brand', methods=['GET', 'POST'])
@login_required
def add_brand():   #obtenemos los datos para agregar marca
    if request.method == 'POST':
        name = request.form['name']
        if check_brand(name):  #Chequeamos que el dato sea correcto
            new_brand = Brands(name=name)
            db.session.add(new_brand)       #Si lo es lo agregamosa la  Database
            db.session.commit()
            flash('Marcas agregada con éxito')
            return redirect(url_for('brands.home'))
    return render_template('add_brand.html')

@brands.route('/delete-brand/<int:id>', methods=['GET'])
@login_required
def delete_brand(id):   #Obtenemos el id de la marca a eliminar
    brand = Brands.query.get_or_404(id)
    db.session.delete(brand)      #Eliminamos la instancia mediante el id 
    db.session.commit()
    flash('Marcas eliminada con éxito')
    return redirect(url_for('brands.home'))


@brands.route('/products-list/<string:brand_name>', methods=['GET'])
@login_required
def list_products(brand_name):  #Obtenemos el id de la marca a eliminar
    brand = Brands.query.filter_by(name=brand_name).first_or_404()  #obtenemos la marca desde la tabla que coincida con la que buscamos eliminar
    products = Products.query.filter_by(brand=brand.name).all() #obtenemos todos los productos cuyo campo marca sea igual a brand.name es decir que pertenezcan a  la misma
    return render_template('product_list.html', brand=brand, products=products)  #redirigimos a un template donde se listan los products por marca
