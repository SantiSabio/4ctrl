# models/tables.py
from utils.db import db  

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    marca = db.Column(db.Integer, db.ForeignKey('marcas.nombre'), nullable=False)

    def __repr__(self):
        return f"Product('{self.nombre}', '{self.marca}', '{self.precio}')"
    
class Marcas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    cant_art = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return  f"Marca ('{self.nombre}' , '{self.cant_art}')"
