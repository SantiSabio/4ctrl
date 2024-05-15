from utils.db import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    precio = db.Column(db.String(100))

    def __init__(self, nombre, marca, precio):
        self.nombre = nombre
        self.marca = marca
        self.precio = precio