from flask_restful import Resource, fields, marshal_with, abort
from models.alumno_model import AlumnoModel
from models import alumnos_data
from schemas import alumnos_post_args, alumnos_patch_args

# Define the data fields for students
alumno_resource_fields = {
    'id': fields.Integer,
    'nombres': fields.String,
    'apellidos': fields.String,
    'matricula': fields.String,
    'promedio': fields.Integer
}

class Alumnos(Resource):
    @marshal_with(alumno_resource_fields)
    def get(self):
        return alumnos_data
    
    @marshal_with(alumno_resource_fields)
    def post(self):
        args = alumnos_post_args.parse_args()
        for alumno in alumnos_data:
            if alumno.matricula == args['matricula']:
                abort(400, message='Ya existe un alumno con la matrícula proporcionada')
        new_alumno = AlumnoModel(**args)
        # new_alumno = AlumnoModel(id=len(alumnos_data) + 1, **args)
        
        print("POST")
        for key, value in new_alumno.__dict__.items():
            print(key, value)
            
        alumnos_data.append(new_alumno)
        return new_alumno, 201

class Alumno(Resource):
    @marshal_with(alumno_resource_fields)
    def get(self, alumno_id):
        alumno = next((al for al in alumnos_data if al.id == alumno_id), None)
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
        return alumno

    @marshal_with(alumno_resource_fields)
    def put(self, alumno_id):
        args = alumnos_post_args.parse_args()
        alumno = next((al for al in alumnos_data if al.id == alumno_id), None)
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
            
        print("PUT")
        for key, value in args.items():
            print(key, value)
        
        alumno.update({
            'id': args['id'],
            'nombres': args['nombres'],
            'apellidos': args['apellidos'],
            'matricula': args['matricula'],
            'promedio': args['promedio']
        })
        return alumno
    
    @marshal_with(alumno_resource_fields)
    def patch(self, alumno_id):
        args = alumnos_patch_args.parse_args()
        alumno = next((al for al in alumnos_data if al.id == alumno_id), None)
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
        for key, value in args.items():
            if value:
                setattr(alumno, key, value)
        return alumno
    
    def delete(self, alumno_id):
        global alumnos_data
        alumno = next((al for al in alumnos_data if al.id == alumno_id), None)
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
        alumnos_data = [al for al in alumnos_data if al.id != alumno_id]
        return {'message': 'Alumno eliminado'}
