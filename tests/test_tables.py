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

    def test_table_brands(self):
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        self.assertIn('brands', tables, "La tabla 'brands' no fue creada")

        columns = inspector.get_columns('brands')
        expected_columns = ['id', 'name','amount_art']
        name_columns = [col['name'] for col in columns]  # Lista por comprensión para obtener las columnas de la tabla
        
        for col in expected_columns:
            self.assertIn(col, name_columns, f'El campo {col} no existe')

    def test_table_products(self):
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        self.assertIn('products', tables, "La tabla 'products' no fue creada")

        columns = inspector.get_columns('products')
        expected_columns = ['id', 'name', 'price', 'brand']
        name_columns = [col['name'] for col in columns]  # Lista por comprensión para obtener las columnas de la tabla
        
        for col in expected_columns:
            self.assertIn(col, name_columns, f'El campo {col} no existe')

if __name__ == '__main__':
    unittest.main()
