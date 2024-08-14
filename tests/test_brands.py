import unittest
from app import create_app
from models.Product import Products
from models.Brand import Brands
from utils.db import db
from models.user import User

class MarcasTestCase(unittest.TestCase):
    # Levantamos una app y creamos DB y sus tablas
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['LOGIN_DISABLED'] = True  # Desactiva la autenticación
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
    
    def test_see_brands(self):
        response = self.client.get('/')  
        print(response)
        self.assertEqual(response.status_code, 200)


    def test_add_marca_post_valid(self):
        # Enviar solicitud POST para agregar una nueva marca
        response = self.client.post('/add-brand', data={
            'name': 'Nueva Marca'}, follow_redirects=True)
        
        # Verifica que la respuesta sea 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la marca se haya agregado correctamente a la base de datos
        added_marca = db.session.execute(db.select(Brands).filter_by(name='Nueva Marca')).scalar_one_or_none()  # Asegúrate de que la consulta sea correcta
        self.assertIsNotNone(added_marca)
        self.assertEqual(added_marca.amount_art, 0)  # Comparar con entero ya que 'amount_art' es un número que  por defecto es 0
        self.assertEqual(added_marca.name, 'Nueva Marca')  # Verifica el name correctamente
        
        # Eliminar la marca agregada para limpiar la base de datos
        db.session.delete(added_marca)
        db.session.commit()


    def test_add_marca_post_invalid(self):
        response = self.client.post('/add-brand', data={
            'name': '',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        

    def test_delete_marca(self):
        marca = Brands(name='Marcas a Eliminar')
        db.session.add(marca)
        db.session.commit()

        marca_id = marca.id
        response = self.client.post(f'/delete-brand/{marca_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la marca ya no existe en la base de datos
        deleted_marca = db.session.execute(db.select(Brands).filter_by(id=marca_id)).scalar_one_or_none()
        self.assertIsNone(deleted_marca)


    def test_list_products(self):
        # Setup test data
        marca1 = Brands(name='Marca de prueba')
        db.session.add(marca1)
        db.session.commit()

        producto1 = Products(name='Prod1', price=123,  brand=marca1.name)
        producto2 = Products(name='Prod2', price=456,  brand=marca1.name)
        db.session.add(producto1)
        db.session.add(producto2)
        db.session.commit()

        # Make the request
        response = self.client.get(f'/products-list/{marca1.name}', follow_redirects=True)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lista de Productos por Marca', response.data)
        self.assertIn(b'Prod1', response.data)  # Check for the presence of product names
        self.assertIn(b'Prod2', response.data)

        # Clean up the database
        db.session.delete(producto1)
        db.session.delete(producto2)
        db.session.commit()
        db.session.delete(marca1)
        db.session.commit()  # Commit the deletion of the brand


if __name__ == '__main__':
    unittest.main()