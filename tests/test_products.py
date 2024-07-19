import unittest
from flask import Flask, url_for
from app import create_app
from models.tables import Productos,Productos
from utils.db import db

class ProductTestCase(unittest.TestCase):
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

    def test_add_marca_get(self):
        response = self.client.get('/add_products')
        self.assertEqual(response.status_code, 200)

    def test_add_marca_post_valid(self):
        response = self.client.post('/marcas/add-product', data={
            'nombre': 'Nueva Productos',
            'cant_art': '5'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_marca_post_invalid(self):
        response = self.client.post('/marcas/add-product', data={
            'nombre': '',
            'cant_art': 'no es un número'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_edit_product(self):
        product = Productos(nombre='Productos Original', marca='pichicho')
        db.session.add(product)
        db.session.commit()
        product_id= product.id

        response = self.client.post(f'/edit/{product.id}', data={'nombre': 'Productos Actualizada','cant_art': 6}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_product=Productos.query.get(product_id)
        self.assertIsNotNone(updated_product)

        self.assertEqual(updated_product.nombre, 'Productos Actualizada')
        self.assertEqual(updated_product.cant_art, 6)
    

    def test_delete_product(self):
        product = Productos(nombre='Productos a Eliminar',)
        db.session.add(product)
        db.session.commit()

        product_id = product.id
        response = self.client.get(f'/delete/{product_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la product ya no existe en la base de datos
        deleted_product = Productos.query.get(product_id)
        self.assertIsNone(deleted_product)

if __name__ == '__main__':
    unittest.main()