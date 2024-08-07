# app.py
from flask import Flask
from utils.db import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/productsdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de la base de datos
    db.init_app(app)

    # Inicialización de Flask-Migrate
    migrate = Migrate(app, db)

    # Registro de los blueprints
    from routes.products import products
    from routes.brands import brands

    app.register_blueprint(products,url_prefix='/products')
    app.register_blueprint(brands, url_prefix='/brands')

    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    
    return app
