import unittest
from utils.security import create_hash, verify_hash

class TestSecurity(unittest.TestCase):

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
