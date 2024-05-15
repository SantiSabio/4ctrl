from flask import Flask
from routes.products import products
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/productsdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.register_blueprint(products)
