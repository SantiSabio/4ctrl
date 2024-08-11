#utils/auth.py
from flask_login import LoginManager
from models.user import User  # Asegúrate de que la clase User esté importada correctamente

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Ruta a la página de login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
