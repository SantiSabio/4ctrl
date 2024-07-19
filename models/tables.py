from utils.db import db  

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)
    marca = db.relationship('Marca', backref=db.backref('productos', lazy=True))
    def __repr__(self):
        return f"Product('{self.nombre}', '{self.marca}', '{self.precio}')"
    
class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    cant_art = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return  f"Marca ('{self.nombre}' , '{self.cant_art}')"