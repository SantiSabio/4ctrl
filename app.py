from flask import Flask
from routes.products import products


app = Flask(__name__)


app.register_blueprint(products)
