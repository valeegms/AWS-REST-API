from flask import request
from flask_restful import Resource, fields, marshal_with, abort
from models.alumno_model import AlumnoModel

from database import db
from schemas import alumnos_post_args, alumnos_patch_args

alumno_resource_fields = {
    'id': fields.Integer,
    'nombres': fields.String,
    'apellidos': fields.String,
    'matricula': fields.String,
    'promedio': fields.Float,
    'fotoPerfilUrl': fields.String,
    'password': fields.String
}

class Alumnos(Resource):
    @marshal_with(alumno_resource_fields)
    def get(self):
        alumnos = AlumnoModel.query.all()
        return alumnos
    
    @marshal_with(alumno_resource_fields)
    def post(self):
        args = alumnos_post_args.parse_args()
        alumno = AlumnoModel.query.filter_by(matricula=args['matricula']).first()
        if alumno:
            abort(400, message='Ya existe un alumno con la matrícula proporcionada')
        new_alumno = AlumnoModel(nombres=args['nombres'], apellidos=args['apellidos'], matricula=args['matricula'], promedio=args['promedio'], fotoPerfilUrl=args['fotoPerfilUrl'], password=args['password'])
        db.session.add(new_alumno)
        db.session.commit()
        return new_alumno, 201

class Alumno(Resource):
    @marshal_with(alumno_resource_fields)
    def get(self, alumno_id):
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
        return alumno

    @marshal_with(alumno_resource_fields)
    def put(self, alumno_id):
        args = alumnos_post_args.parse_args()
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
            
        for key, value in args.items():
            setattr(alumno, key, value)
        db.session.commit()
        return alumno
    
    @marshal_with(alumno_resource_fields)
    def patch(self, alumno_id):
        args = alumnos_patch_args.parse_args()
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
        for key, value in args.items():
            if value:
                setattr(alumno, key, value)
        db.session.commit()
        return alumno
    
    def delete(self, alumno_id):
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
        db.session.delete(alumno)
        db.session.commit()
        return {'message': 'Alumno eliminado'}

class AlumnoFotoPerfil(Resource):
    def patch(self, alumno_id, foto_perfil_url):
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
        alumno.fotoPerfilUrl = foto_perfil_url
        db.session.commit()
        return {'message': 'Foto de perfil actualizada'}