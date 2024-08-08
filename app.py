# app.py
from flask import Flask
from utils.db import db
from flask_migrate import Migrate
from utils.auth import login_manager  # Asegúrate de que esta línea esté correcta

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/productsdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    
    # Inicialización de la base de datos
    db.init_app(app)
    
    # Inicialización de Flask-Migrate
    migrate = Migrate(app, db)
    
    # Inicialización de Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Asegúrate de establecer la ruta de inicio de sesión

    # Registro de los blueprints
    from routes.products import products
    from routes.marcas import marcas
    from routes.auth import auth
    
    app.register_blueprint(products)
    app.register_blueprint(marcas, url_prefix='/marcas')
    app.register_blueprint(auth, url_prefix='/auth')
    
    return app
