import unittest
from app import create_app
from models.tables import Productos,Marcas
from utils.db import db
from sqlalchemy import select



class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    #def tearDown(self):
    #    db.session.remove()
    #    db.drop_all()
    #    self.app_context.pop()

    def test_ver_productos(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_add_marca_get(self):
        response = self.client.get('/add_products')
        self.assertEqual(response.status_code, 200)

    def test_add_product_post_valid(self):

        marca=Marcas(nombre='Nueva Marcas', cant_art=51)
        db.session.add(marca)
        # Asegúrate de que la ruta sea '/add_products' y no '/marcas/add-product'
        response = self.client.post('/add_products', data={
            'nombre': 'Nuevo Producto',
            'precio': 5.00,  # Asegúrate de que el tipo de dato coincida con el modelo
            'marca': 'Nueva Marcas'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Verifica que el producto se haya agregado correctamente a la base de datos
        added_product = db.session.execute(db.select(Productos).filter_by(nombre='Nuevo Producto')).scalar_one_or_none()
        self.assertIsNotNone(added_product)
        self.assertEqual(added_product.precio, 5.00)
        self.assertEqual(added_product.marca, 'Nueva Marcas')

        db.session.delete(added_product)
        db.session.commit()


    def test_add_product_post_invalid(self):
        # Enviar datos inválidos
        response = self.client.post('/add_products', data={
            'nombre': '',  # Nombre vacío
            'precio': 'no es un número',  # Precio no válido
            'marca': 'Nueva Marcas'  # Marca válida para asegurar que la validación de marca no sea el problema
        }, follow_redirects=True)
        
        # Verifica que la respuesta sea la esperada, normalmente una página de error o el mismo formulario
        self.assertEqual(response.status_code, 200)

        # Verifica que el producto no se haya agregado a la base de datos

        added_product = db.session.execute(db.select(Productos).filter_by(nombre='')).scalar_one_or_none()
        self.assertIsNone(added_product)

        
    def test_edit_product(self):
        product = Productos(nombre='Productos Original',precio=5 ,marca='Nueva Marcas')
        db.session.add(product)
        db.session.commit()
        product_id= product.id

        response = self.client.post(f'/edit/{product.id}', data={'nombre': 'Productos Actualizada','precio': 6, 'marca':'Nueva Marcas'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_product=db.session.get(Productos,product_id)
        self.assertIsNotNone(updated_product)

        self.assertEqual(updated_product.nombre, 'Productos Actualizada')
        self.assertEqual(updated_product.precio, 6)

        db.session.delete(updated_product)
        db.session.commit()

    

    def test_delete_product(self):
        product = Productos(nombre='Productos a Eliminar',precio=500,marca='Nueva Marcas')
        db.session.add(product)
        db.session.commit()

        product_id = product.id
        response = self.client.get(f'/delete/{product_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la product ya no existe en la base de datos
        deleted_product = db.session.get(Productos,product_id)
        self.assertIsNone(deleted_product)

if __name__ == '__main__':
    unittest.main()