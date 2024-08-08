import unittest
from app import create_app
from models.Product import Product
from models.Brand import Brand
from utils.db import db

class ProductTestCase(unittest.TestCase):
    # Se ejecuta antes de cada prueba
    def setUp(self):
        self.app = create_app()  # Crea una instancia de la aplicación Flask
        self.app.config['TESTING'] = True  # Activa el modo de pruebas
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usa una base de datos en memoria para pruebas
        self.client = self.app.test_client()  # Crea un cliente de prueba para hacer solicitudes HTTP
        self.app_context = self.app.app_context()  # Crea un contexto de aplicación
        self.app_context.push()  # Empuja el contexto de la aplicación
        db.create_all()  # Crea todas las tablas en la base de datos en memoria

    # Se ejecuta después de cada prueba
    def tearDown(self):
        db.session.remove()  # Elimina la sesión actual de la base de datos
        db.drop_all()  # Elimina todas las tablas de la base de datos
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_list_products(self):
        response = self.client.get('/')  # Realiza una solicitud GET a la ruta raíz
        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado de la respuesta sea 200 (OK)

    def test_add_product_get(self):
        response = self.client.get('/add_products')  # Realiza una solicitud GET a la ruta para agregar productos
        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado de la respuesta sea 200 (OK)

    def test_add_product_post_valid(self):
        # Agrega una marca válida a la base de datos
        brand = Brand(name='Nueva Marca', ammount_art=51)
        db.session.add(brand)
        db.session.commit()
        
        # Realiza una solicitud POST para agregar un producto válido
        response = self.client.post('/add_products', data={
            'name': 'Nuevo Producto',
            'price': 5.00,
            'brand': 'Nueva Marca'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea exitosa

        # Verifica que el producto se haya agregado a la base de datos
        added_product = db.session.execute(db.select(Product).filter_by(name='Nuevo Producto')).scalar_one_or_none()
        self.assertIsNotNone(added_product)  # Asegúrate de que el producto no sea None
        self.assertEqual(added_product.price, 5.00)
        self.assertEqual(added_product.brand, 'Nueva Marca')

        # Elimina el producto después de la prueba
        db.session.delete(added_product)
        db.session.commit()

    def test_add_product_post_invalid(self):
        # Realiza una solicitud POST con datos inválidos
        response = self.client.post('/add_products', data={
            'name': '',  # Nombre vacío
            'price': 'esto no es un número',  # Precio no válido
            'brand': 'Nueva Marca'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea exitosa

        # Verifica que el producto no se haya agregado a la base de datos
        added_product = db.session.execute(db.select(Product).filter_by(name='')).scalar_one_or_none()
        self.assertIsNone(added_product)

    def test_edit_product(self):
        # Agrega un producto para editar
        product = Product(name='Producto Original', price=5, brand='Nueva Marca')
        db.session.add(product)
        db.session.commit()
        product_id = product.id

        # Realiza una solicitud POST para editar el producto
        response = self.client.post(f'/edit/{product.id}', data={'name': 'Producto Actualizado','price': 6, 'brand':'Nueva Marca'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea exitosa

        # Verifica que el producto se haya actualizado correctamente
        updated_product = db.session.get(Product, product_id)
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product.name, 'Producto Actualizado')
        self.assertEqual(updated_product.price, 6)

        # Elimina el producto después de la prueba
        db.session.delete(updated_product)
        db.session.commit()

    def test_delete_product(self):
        # Agrega un producto para eliminar
        product = Product(name='Producto a Eliminar', price=500, brand='Nueva Marca')
        db.session.add(product)
        db.session.commit()

        product_id = product.id
        # Realiza una solicitud GET para eliminar el producto
        response = self.client.get(f'/delete/{product_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea exitosa
        
        # Verifica que el producto haya sido eliminado de la base de datos
        deleted_product = db.session.get(Product, product_id)
        self.assertIsNone(deleted_product)

