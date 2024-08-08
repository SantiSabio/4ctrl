import unittest
from flask import current_app
from app import create_app
import os

class AppTestCase(unittest.TestCase):
#Levantamos la app y le creamos contexto
    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
#Chequear si el current app es no vacio, es decir que exista
    def test_app(self):
        self.assertIsNotNone(current_app)

if __name__ == '__main__':
    unittest.main()
    