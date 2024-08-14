import unittest
from app import create_app, db

class DbTestCase(unittest.TestCase):

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
