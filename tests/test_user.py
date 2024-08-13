import unittest
from models.user import User

class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.user = User(username="testuser")

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
