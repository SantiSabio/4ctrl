import unittest
from app import create_app, db
from models.product import Productos


class MarcasTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_ver_productos(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_add_producto_get(self):
        response = self.client.get('/add_products')
        self.assertEqual(response.status_code, 200)

"""    def test_add_producto_post_valid(self):
        response = self.client.post('/add_products', data={
            'nombre': 'Nuevo Producto',
            'cant_art': '5'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_producto_post_invalid(self):
        response = self.client.post('/add_products', data={
            'nombre': '',
            'cant_art': 'no es un número'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_edit_producto(self):
        producto = Productos(nombre='Producto Original', cant_art=5)
        db.session.add(producto)
        db.session.commit()
        producto_id = producto.id

        response = self.client.post(f'/marcas/edit-marca/{producto.id}', data={'nombre': 'Marca Actualizada','cant_art': 6}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_marca=Productos.query.get(producto_id)
        self.assertIsNotNone(updated_marca)

        self.assertEqual(updated_marca.nombre, 'Marca Actualizada')
        self.assertEqual(updated_marca.cant_art, 6)       

    def test_delete_marca(self):
        marca = Marca(nombre='Marca a Eliminar', cant_art=5)
        db.session.add(marca)
        db.session.commit()

        marca_id = marca.id
        response = self.client.get(f'/marcas/delete-marca/{marca_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la marca ya no existe en la base de datos
        deleted_marca = Marca.query.get(marca_id)
        self.assertIsNone(deleted_marca)

"""