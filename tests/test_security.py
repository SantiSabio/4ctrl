import unittest
from app import create_app, db
from utils.security import create_hash, verify_hash

class TestSecurity(unittest.TestCase):

    # Se ejecuta antes de cada prueba
    def setUp(self):
        self.app = create_app()  # Crea una instancia de la aplicación Flask
        self.app.config['TESTING'] = True  # Activa el modo de pruebas
        self.app.config['LOGIN_DISABLED'] = True  # Desactiva la autenticación
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usa una base de datos en memoria para pruebas
        self.client = self.app.test_client()  # Crea un cliente de prueba para hacer solicitudes HTTP
        self.app_context = self.app.app_context()  # Crea un contexto de aplicación
        self.app_context.push()  # Empuja el contexto de la aplicación
        db.create_all()  # Crea todas las tablas en la base de datos en memoria


    def test_create_hash(self):
        password = "my_secret_password"
        hashed_password = create_hash(password)

        # Verificar que el hash no coincida con la constraseña 
        self.assertNotEqual(password, hashed_password)
        # Verifica que se esté utilizando el algoritmo por defecto de Werkzeug (pbkdf2 con SHA-256)
        self.assertTrue(hashed_password.startswith('pbkdf2:sha'))

    def test_verify_hash(self):
        password = "my_secret_password"
        hashed_password = create_hash(password)

        # Con password correcto
        self.assertTrue(verify_hash(hashed_password, password))

        # Con password incorrecto
        self.assertFalse(verify_hash(hashed_password, "wrong_password"))

if __name__ == '__main__':
    unittest.main()
