import unittest
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_alumno(self):
        # Test adding a new student (alumno)
        response = self.app.post('/alumnos', data=json.dumps({
            'id': 1,
            'nombres': 'Juan',
            'apellidos': 'Perez',
            'matricula': '12345',
            'promedio': 85
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Juan', response.data)

    def test_get_alumnos(self):
        # Test retrieving the list of students (alumnos)
        response = self.app.get('/alumnos')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_update_alumno(self):
        # First, add a new student to update
        response = self.app.post('/alumnos', data=json.dumps({
            'id': 2,
            'nombres': 'Ana',
            'apellidos': 'Garcia',
            'matricula': '67890',
            'promedio': 90
        }), content_type='application/json')
        alumno_id = json.loads(response.data)['id']

        # Test updating the student's information
        response = self.app.put(f'/alumnos/{alumno_id}', data=json.dumps({
            'nombres': 'Ana Maria',
            'apellidos': 'Garcia',
            'matricula': '67890',
            'promedio': 95
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ana Maria', response.data)

    def test_delete_alumno(self):
        # First, add a new student to delete
        response = self.app.post('/alumnos', data=json.dumps({
            'id': 3,
            'nombres': 'Carlos',
            'apellidos': 'Lopez',
            'matricula': 'A54321',
            'promedio': 88
        }), content_type='application/json')
        alumno_id = json.loads(response.data)['id']

        # Test deleting the student
        response = self.app.delete(f'/alumnos/{alumno_id}')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Carlos', response.data)

    def test_add_profesor(self):
        # Test adding a new teacher (profesor)
        response = self.app.post('/profesores', data=json.dumps({
            'id': 1,
            'numeroEmpleado': '001',
            'nombres': 'Luis',
            'apellidos': 'Hernandez',
            'horasClase': 20
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Luis', response.data)

    def test_get_profesores(self):
        # Test retrieving the list of teachers (profesores)
        response = self.app.get('/profesores')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_update_profesor(self):
        # First, add a new teacher to update
        response = self.app.post('/profesores', data=json.dumps({
            'id': 2,
            'numeroEmpleado': '002',
            'nombres': 'Maria',
            'apellidos': 'Fernandez',
            'horasClase': 15
        }), content_type='application/json')
        profesor_id = json.loads(response.data)['id']

        # Test updating the teacher's information
        response = self.app.put(f'/profesores/{profesor_id}', data=json.dumps({
            'numeroEmpleado': '002',
            'nombres': 'Maria Isabel',
            'apellidos': 'Fernandez',
            'horasClase': 18
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Maria Isabel', response.data)

    def test_delete_profesor(self):
        # First, add a new teacher to delete
        response = self.app.post('/profesores', data=json.dumps({
            'id': 3,
            'numeroEmpleado': '003',
            'nombres': 'Jorge',
            'apellidos': 'Martinez',
            'horasClase': 10
        }), content_type='application/json')
        profesor_id = json.loads(response.data)['id']

        # Test deleting the teacher
        response = self.app.delete(f'/profesores/{profesor_id}')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Jorge', response.data)

if __name__ == '__main__':
    unittest.main()
