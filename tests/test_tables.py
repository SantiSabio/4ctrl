import unittest
from flask import current_app
from app import create_app
from utils.db import db

class DbTestCase(unittest.TestCase):
    def setUp(self):
        # Crear una instancia de la aplicación y establecer la configuración para pruebas
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    #def tearDown(self):
    # Limpiar la base de datos después de cada prueba
    #   db.session.remove()
    #  db.drop_all()
    # self.app_context.pop()

    def test_table_marcas(self):
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        self.assertIn('marcas', tables, "La tabla 'marca' no fue creada")

        columns = inspector.get_columns('marcas')
        expected_columns = ['id', 'nombre']
        name_columns = [col['name'] for col in columns]  # Lista por comprensión para obtener las columnas de la tabla
        
        for col in expected_columns:
            self.assertIn(col, name_columns, f'El campo {col} no existe')

    def test_table_productos(self):
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        self.assertIn('productos', tables, "La tabla 'productos' no fue creada")

        columns = inspector.get_columns('productos')
        expected_columns = ['id', 'nombre', 'precio', 'marca']
        name_columns = [col['name'] for col in columns]  # Lista por comprensión para obtener las columnas de la tabla
        
        for col in expected_columns:
            self.assertIn(col, name_columns, f'El campo {col} no existe')

if __name__ == '__main__':
    unittest.main()
