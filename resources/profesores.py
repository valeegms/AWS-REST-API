from flask_restful import Resource, fields, marshal_with, abort

from database import db
from schemas import profesores_post_args, profesores_patch_args
from models.profesor_model import ProfesorModel

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
        profesores = ProfesorModel.query.all()
        return profesores
    
    @marshal_with(profesor_resource_fields)
    def post(self):
        args = profesores_post_args.parse_args()
        if ProfesorModel.query.filter_by(numeroEmpleado=args['numeroEmpleado']).first():
            abort(400, message='Ya existe un profesor con el número de empleado proporcionado')
        new_profesor = ProfesorModel(**args)
        db.session.add(new_profesor)
        db.session.commit()
        return new_profesor, 201

class Profesor(Resource):
    @marshal_with(profesor_resource_fields)
    def get(self, profesor_id):
        profesor = ProfesorModel.query.filter_by(id=profesor_id).first()
        if not profesor:
            abort(404, message='No se encontró el profesor con el ID proporcionado')
        return profesor

    @marshal_with(profesor_resource_fields)
    def put(self, profesor_id):
        args = profesores_post_args.parse_args()
        profesor = ProfesorModel.query.filter_by(id=profesor_id).first()
        if profesor:
            for key, value in args.items():
                setattr(profesor, key, value)
        else:
            profesor = ProfesorModel(id=profesor_id, **args)
            db.session.add(profesor)
            
        db.session.commit()
        return profesor
    
    @marshal_with(profesor_resource_fields)
    def patch(self, profesor_id):
        args = profesores_post_args.parse_args()
        profesor = ProfesorModel.query.filter_by(id=profesor_id).first()
        if not profesor:
            abort(404, message='No se encontró el profesor con el ID proporcionado')
        for key, value in args.items():
            if value:
                setattr(profesor, key, value)
        db.session.commit()
        return profesor

    def delete(self, profesor_id):
        profesor = ProfesorModel.query.filter_by(id=profesor_id).first()
        if not profesor:
            abort(404, message='No se encontró el profesor con el ID proporcionado')
        db.session.delete(profesor)
        db.session.commit()
        return {'message': 'Profesor eliminado'}
