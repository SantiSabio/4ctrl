from app import db


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    amount_art = db.Column(db.Integer, nullable=False,default = 0)


    products = db.relationship('Products', backref='brand_ref', lazy=True)
    def __repr__(self):
        return  f"Marca ('{self.name}' , '{self.amount_art}')"