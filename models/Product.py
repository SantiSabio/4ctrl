from utils.db import db

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(100), db.ForeignKey('brands.id'), nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.brand}', '{self.price}')"