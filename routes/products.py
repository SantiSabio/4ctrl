from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from models.Product import Products
from models.Brand import Brands
from app import db

products = Blueprint('products', __name__)


#Ruta principal donde hace un display del home de productos
@products.route('/')
@login_required
def home():
    products = Products.query.all()
    return render_template("products.html", products=products)

#Obtenemos todos los productos de la base de datos y lo enviamos como  json al html  para su display
@products.route('/get_brands', methods=['GET'])
@login_required
def get_brands():
    query = request.args.get('q', '')
    brands = Brands.query.filter(Brands.nombre.ilike(f'%{query}%')).all()
    return jsonify([{'nombre': brand.nombre} for brand in brands])

#definimos estructura logica para que el name brand y price sean correctos y aceptados por la  DataBase
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
@login_required
def add_product():     #Tomamos los  valores del formulario correspondiente
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        price = request.form['price']

        brand_exists = Brands.query.filter_by(name=brand).first()  #Chequeamos que la marca exista antes de agregar el producto
        if not brand_exists:
            flash('La marca seleccionada no existe')
            return redirect(url_for('products.add_product'))

        if check(name, brand, price):  #si los valores son correctos agregamos el prod a la tabla de products
            new_product = Products(name=name, brand=brand, price=float(price))
            db.session.add(new_product)
            brand_exists.amount_art += 1  #Como agregamos un producto nuevo a la marca, la cantidad de productos nuevos es +1

            db.session.commit()
            
            flash('Producto agregado con éxito')
            return redirect(url_for('products.home'))
        else: #Si los valores no son correctos volvemos al formulario de agregar producto
            brands = Brands.query.all()
            return render_template('products.html', nombre=name, marca=brand, precio=price, marcas=brands)

    brands = Brands.query.all()
    return render_template('products.html', marcas=brands)

@products.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Products.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        price = request.form['price']

        # Verificamos si la marca existe
        brand_exists = Brands.query.filter_by(name=brand).first()
        if not brand_exists:
            flash('La marca seleccionada no existe')
            return redirect(url_for('products.edit_product', id=id))

        # Validación de los datos del producto
        if check(name, brand, price):
            product.name = name
            product.brand = brand
            product.price = float(price)
            db.session.commit()  # Guardamos los cambios en la base de datos
            flash('Producto actualizado con éxito')
            return redirect(url_for('products.home'))  # Redirigimos a la pagina de inicio de productos
        else:
            flash('Error en los datos ingresados')
            return render_template('edit_product.html', product=product, nombre=name, marca=brand, precio=price)

    # Renderiza el formulario para editar el producto con los datos actuales
    return render_template('edit_product.html', product=product)



@products.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete_product(id):  #Obtenemos el id del producto a eliminar

    product = Products.query.get_or_404(id)  #Buscamos el producto y lo eliminamos de la DataBase
    db.session.delete(product)

    brand = Brands.query.filter_by(name=product.brand).first()   #Buscamos la marca y reducimos la cantidad de articulos en 1
    brand.amount_art -= 1

    db.session.commit()
    flash('Producto eliminado con éxito')
    return redirect(url_for('products.home'))
