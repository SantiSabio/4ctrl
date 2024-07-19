import unittest
from flask import current_app
from app import create_app
from utils.db import db

#testeamos que la app crea la base de  datos y que las tablas estan creadas con sus respectivos campos


class DbTestCase(unittest.TestCase):
    def setUp(self):
        self.app= create_app()
        self.app.config['TESTING']=True
        self.app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///:memory'
        self.client= self.app.test_client()
        self.app_context= self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_table_marca(self):
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        self.assertIn('marca', tables, "La tabla 'marca' no fue creada")
        self.assertIn('productos', tables, "La tabla 'marca' no fue creada")

        columns=  inspector.get_columns('marca')
        expected_columns= ['id','nombre','cant_art']
        name_columns= [col['name'] for col in columns] #lista por comprension para obtener las columans de la tabla
        
        for col in expected_columns:
            self.assertIn(col,name_columns,f'El campo {col}  no existe')

    def test_table_productos(self):
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        self.assertIn('productos', tables, "La tabla 'productos' no fue creada")

        columns=  inspector.get_columns('productos')
        expected_columns= ['id','nombre','precio','marca_id']
        name_columns= [col['name'] for col in columns] #lista por comprension para obtener las columans de la tabla
        
        for col in expected_columns:
            self.assertIn(col,name_columns,f'El campo {col}  no existe')

if __name__ == '__main__':
    unittest.main()