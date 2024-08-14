import unittest
from models.user import User
from app import create_app, db

class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.user = User(username="testuser")
        self.app = create_app()  # Crea una instancia de la aplicación Flask
        self.app.config['TESTING'] = True  # Activa el modo de pruebas
        self.app.config['LOGIN_DISABLED'] = True  # Desactiva la autenticación
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usa una base de datos en memoria para pruebas
        self.client = self.app.test_client()  # Crea un cliente de prueba para hacer solicitudes HTTP
        self.app_context = self.app.app_context()  # Crea un contexto de aplicación
        self.app_context.push()  # Empuja el contexto de la aplicación
        db.create_all()  # Crea todas las tablas en la base de datos en memoria


    def test_set_password(self):
        # Creación del hash
        self.user.set_password("mypassword")
        self.assertIsNotNone(self.user.password)
        self.assertNotEqual(self.user.password, "mypassword")

    def test_check_password(self):
        # Verificación de la contraseña
        self.user.set_password("mypassword")
        self.assertTrue(self.user.check_password("mypassword"))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_user_repr(self):
        self.assertEqual(repr(self.user), "<User testuser>")

if __name__ == '__main__':
    unittest.main()
