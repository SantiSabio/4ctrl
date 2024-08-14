import os
import unittest
from sqlalchemy import text
from app import create_app, db

class ConnectionTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Remover la sesión
        db.session.remove()
        self.app_context.pop()

    def test_db_connection(self):
        # Ejecuta una consulta básica
        result = db.session.query(text("'Hello world'")).one()
        self.assertEqual(result[0], 'Hello world')
        

if __name__ == '__main__':
    unittest.main()
