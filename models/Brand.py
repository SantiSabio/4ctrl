from utils.db import db


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ammount_art = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return  f"Marca ('{self.name}' , '{self.ammount_art}')"