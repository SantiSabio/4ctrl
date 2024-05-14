from flask import Flask
from routes.products import products
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ''

SQLAlchemy(app)

app.register_blueprint(products)
