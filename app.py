from flask import Flask
from routes.products import products
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://santi:password@localhost/productos'

SQLAlchemy(app)

app.register_blueprint(products)
