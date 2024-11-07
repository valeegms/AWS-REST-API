from flask_restful import Resource, fields, marshal_with, abort
from models import profesores_data
from schemas import profesores_post_args, profesores_patch_args
from models.profesor_model import ProfesorModel

# Define the data fields for teachers
profesor_resource_fields = {
    'id': fields.Integer,
    'numeroEmpleado': fields.Integer,
    'nombres': fields.String,
    'apellidos': fields.String,
    'horasClase': fields.Integer
}

class Profesores(Resource):
    @marshal_with(profesor_resource_fields)
    def get(self):
        return profesores_data
    
    @marshal_with(profesor_resource_fields)
    def post(self):
        args = profesores_post_args.parse_args()
        for profesor in profesores_data:
            if profesor.numeroEmpleado == args['numeroEmpleado']:
                abort(400, message='Ya existe un profesor con el número de empleado proporcionado')
        new_profesor = ProfesorModel(**args)
        # new_profesor = ProfesorModel(id=len(profesores_data) + 1, **args)
        profesores_data.append(new_profesor)
        return new_profesor, 201

class Profesor(Resource):
    @marshal_with(profesor_resource_fields)
    def get(self, profesor_id):
        profesor = next((prof for prof in profesores_data if prof.id == profesor_id), None)
        if not profesor:
            abort(404, message='No se encontró el profesor con el ID proporcionado')
        return profesor

    @marshal_with(profesor_resource_fields)
    def put(self, profesor_id):
        args = profesores_post_args.parse_args()
        profesor = next((prof for prof in profesores_data if prof.id == profesor_id), None)
        if not profesor:
            abort(404, message='No se encontró el profesor con el ID proporcionado')
        profesor.update({
            'id': args['id'],
            'numeroEmpleado': args['numeroEmpleado'],
            'nombres': args['nombres'],
            'apellidos': args['apellidos'],
            'horasClase': args['horasClase']
        })
        return profesor
    
    @marshal_with(profesor_resource_fields)
    def patch(self, profesor_id):
        args = profesores_patch_args.parse_args()
        profesor = next((prof for prof in profesores_data if prof.id == profesor_id), None)
        if not profesor:
            abort(404, message='No se encontró el profesor con el ID proporcionado')
        for key, value in args.items():
            if value:
                setattr(profesor, key, value)
        return profesor

    def delete(self, profesor_id):
        global profesores_data
        profesor = next((prof for prof in profesores_data if prof.id == profesor_id), None)
        if not profesor:
            abort(404, message='No se encontró el profesor con el ID proporcionado')
        profesores_data = [prof for prof in profesores_data if prof.id != profesor_id]
        return {'message': 'Profesor eliminado'}
