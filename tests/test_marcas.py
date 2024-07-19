import unittest
from flask import Flask, url_for
from app import create_app
from models.tables import Marcas
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

    #def tearDown(self):
    #    db.session.remove()
    #    db.drop_all()
    #   self.app_context.pop()

    def test_ver_marcas(self):
        response = self.client.get('/marcas/')  
        self.assertEqual(response.status_code, 200)

    def test_add_marca_get(self):
        response = self.client.get('/marcas/add-marca')
        self.assertEqual(response.status_code, 200)

    def test_add_marca_post_valid(self):
        # Enviar solicitud POST para agregar una nueva marca
        response = self.client.post('/marcas/add-marca', data={
            'nombre': 'Nueva Marca',  # Asegúrate de que el nombre sea consistente
            'cant_art': '5'
        }, follow_redirects=True)
        
        # Verifica que la respuesta sea 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la marca se haya agregado correctamente a la base de datos
        added_marca = Marcas.query.filter_by(nombre='Nueva Marca').first()  # Asegúrate de que la consulta sea correcta
        self.assertIsNotNone(added_marca)
        self.assertEqual(added_marca.cant_art, 5)  # Comparar con entero ya que 'cant_art' es un número
        self.assertEqual(added_marca.nombre, 'Nueva Marca')  # Verifica el nombre correctamente
        
        # Eliminar la marca agregada para limpiar la base de datos
        db.session.delete(added_marca)
        db.session.commit()



    def test_add_marca_post_invalid(self):
        response = self.client.post('/marcas/add-marca', data={
            'nombre': '',
            'cant_art': 'no es un número'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_edit_marca(self):
        marca = Marcas(nombre='Marcas Original', cant_art=5)
        db.session.add(marca)
        db.session.commit()
        marca_id= marca.id

        response = self.client.post(f'/marcas/edit-marca/{marca.id}', data={'nombre': 'Marcas Actualizada','cant_art': 6}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        updated_marca=Marcas.query.get(marca_id)
        self.assertIsNotNone(updated_marca)

        self.assertEqual(updated_marca.nombre, 'Marcas Actualizada')
        self.assertEqual(updated_marca.cant_art, 6)

        db.session.delete(updated_marca)
        db.session.commit()


    def test_delete_marca(self):
        marca = Marcas(nombre='Marcas a Eliminar', cant_art=5)
        db.session.add(marca)
        db.session.commit()

        marca_id = marca.id
        response = self.client.get(f'/marcas/delete-marca/{marca_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la marca ya no existe en la base de datos
        deleted_marca = Marcas.query.get(marca_id)
        self.assertIsNone(deleted_marca)

if __name__ == '__main__':
    unittest.main()