import unittest
from sqlalchemy import text
from app import create_app, db

class ConnectionTestCase(unittest.TestCase):
   
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

 
    def test_db_connection(self):
        # Ejecuta una consulta básica
        result = db.session.query(text("'Hello world'")).one()
        self.assertEqual(result[0], 'Hello world')
        

if __name__ == '__main__':
    unittest.main()
