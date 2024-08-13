#models/user.py
from utils.db import db
from utils.security import create_hash, verify_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password = create_hash(password)

    def check_password(self, password):
        return verify_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
