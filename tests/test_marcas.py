import unittest
from flask import Flask, url_for
from app import create_app
from models.tables import Marca
from utils.db import db

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

    def test_ver_marcas(self):
        response = self.client.get('/marcas/')
        self.assertEqual(response.status_code, 200)

    def test_add_marca_get(self):
        response = self.client.get('/marcas/add-marca')
        self.assertEqual(response.status_code, 200)

    def test_add_marca_post_valid(self):
        response = self.client.post('/marcas/add-marca', data={
            'nombre': 'Nueva Marca',
            'cant_art': '5'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_marca_post_invalid(self):
        response = self.client.post('/marcas/add-marca', data={
            'nombre': '',
            'cant_art': 'no es un número'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_edit_marca(self):
        marca = Marca(nombre='Marca Original', cant_art=5)
        db.session.add(marca)
        db.session.commit()
        marca_id= marca.id

        response = self.client.post(f'/marcas/edit-marca/{marca.id}', data={'nombre': 'Marca Actualizada','cant_art': 6}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_marca=Marca.query.get(marca_id)
        self.assertIsNotNone(updated_marca)

        self.assertEqual(updated_marca.nombre, 'Marca Actualizada')
        self.assertEqual(updated_marca.cant_art, 6)
<<<<<<< Updated upstream
=======
    
>>>>>>> Stashed changes

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

if __name__ == '__main__':
    unittest.main()