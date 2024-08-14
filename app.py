# app.py
from flask import Flask
from utils.db import db
from flask_migrate import Migrate
from utils.auth import login_manager
from datetime import timedelta

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/productsdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración del tiempo de sesión
    app.permanent_session_lifetime = timedelta(minutes=5)  # Tiempo de expiración de la sesión
    
    # Inicialización de la base de datos
    db.init_app(app)

    # Inicialización de Flask-Migrate
    migrate = Migrate(app, db)

    # Inicialización de Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Ruta de inicio de sesión

    # Registro de los blueprints
    from routes.products import products
    from routes.brands import brands
    from routes.auth import auth

    app.register_blueprint(products,url_prefix='/products')
    app.register_blueprint(brands)
    app.register_blueprint(auth, url_prefix='/auth')

    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    
    return app
