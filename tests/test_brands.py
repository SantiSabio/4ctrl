import unittest
from app import create_app, db
from models.Product import Products
from models.Brand import Brands

class MarcasTestCase(unittest.TestCase):
   
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


    def test_see_brands(self):
        # Verifica que se devuelva la página principal
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


    def test_add_brand_post_valid(self):
        # Enviar solicitud POST para agregar una nueva marca
        response = self.client.post(
            '/add-brand',
            data={'name': 'Nueva Marca'},
            follow_redirects=True
            )
        
        # Verifica que la respuesta sea 200 (ok)
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la marca se haya agregado correctamente a la base de datos
        added_marca = db.session.execute(db.select(Brands).filter_by(name='Nueva Marca')).scalar_one_or_none()  # Asegura que la consulta sea correcta
        self.assertIsNotNone(added_marca)
        self.assertEqual(added_marca.amount_art, 0)  # Comparar con entero ya que 'amount_art' es un número que por defecto es 0
        self.assertEqual(added_marca.name, 'Nueva Marca')  # Verifica el nombre
        
        # Limpia la base de datos
        db.session.delete(added_marca)
        db.session.commit()


    def test_add_brand_post_invalid(self):
        response = self.client.post(
            '/add-brand',
            data={'name': ''},
            follow_redirects=True
            )
        self.assertEqual(response.status_code, 200)
        

    def test_delete_brand(self):
        # Datos del test
        brand = Brands(name='Marca a Eliminar')
        db.session.add(brand)
        db.session.commit()

        brand_id = brand.id
        response = self.client.post(f'/delete-brand/{brand_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la marca ya no existe en la base de datos
        deleted_marca = db.session.execute(db.select(Brands).filter_by(id=brand_id)).scalar_one_or_none()
        self.assertIsNone(deleted_marca)


    def test_list_products(self):
        # Datos del test
        marca1 = Brands(name='Marca de prueba')
        db.session.add(marca1)
        db.session.commit()

        producto1 = Products(name='Prod1', price=123,  brand=marca1.name)
        producto2 = Products(name='Prod2', price=456,  brand=marca1.name)
        db.session.add(producto1)
        db.session.add(producto2)
        db.session.commit()

        # Pedido
        response = self.client.get(f'/products-list/{marca1.name}', follow_redirects=True)

        # Respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lista de Productos por Marca', response.data)
        self.assertIn(b'Prod1', response.data)  # Verifica la presencia de nombres de productos
        self.assertIn(b'Prod2', response.data)

        # Limpia la BD
        db.session.delete(producto1)
        db.session.delete(producto2)
        db.session.commit()
        db.session.delete(marca1)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()