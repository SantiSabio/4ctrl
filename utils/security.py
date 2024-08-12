# utils/security.py
from werkzeug.security import generate_password_hash, check_password_hash

def create_hash(password):
    return generate_password_hash(password)

def verify_hash(stored, provided):
    return check_password_hash(stored, provided)
