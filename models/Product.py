from utils.db import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.Integer, db.ForeignKey('brand.name'), nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.brand}', '{self.price}')"