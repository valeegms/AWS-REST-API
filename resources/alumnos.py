from os import getenv, remove
from tempfile import NamedTemporaryFile
import time
import uuid
from flask import Response, json, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort
from werkzeug.utils import secure_filename
from boto3.dynamodb.conditions import Attr

from models.alumno_model import AlumnoModel
from database import db
from schemas import alumnos_post_args, alumnos_patch_args
from utils.aws import publish_message_to_sns, put_item_to_dynamodb, random_string, scan_table, update_item_in_dynamodb, upload_file_to_s3

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
    def post(self, alumno_id):
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
            
        if 'foto' not in request.files:
            abort(400, message='No se proporcionó la foto de perfil')
        photo = request.files['foto']
        if photo.filename == '':
            abort(400, message='No se seleccionó un archivo')
        
        try:
            with NamedTemporaryFile(delete=False) as tmp:
                photo.save(tmp.name)
                file_path = tmp.name
                filename = secure_filename(photo.filename)
                
                upload_file_to_s3(file_path, filename)
                
            alumno.fotoPerfilUrl = f"https://{getenv('BUCKET_NAME')}.s3.amazonaws.com/{filename}"

            db.session.commit()
        except Exception as e:
            return jsonify({
                "error": "Ocurrió un error al subir la foto de perfil",
                "details": str(e)
            }), 500
        finally:
            tmp.close()
            remove(file_path)
        return Response(
            json.dumps({"fotoPerfilUrl": alumno.fotoPerfilUrl}),
            status=200,
            mimetype="application/json"
        )
        
class AlumnoSendEmail(Resource):
    def post(self, alumno_id):
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
        publish_message_to_sns(f"La calificación del alumno {alumno.nombres} {alumno.apellidos} con matrícula {alumno.matricula} es {alumno.promedio}", getenv('TOPIC_ARN'))
        return jsonify({
            "message": "Mensaje enviado correctamente"
        })
        
class AlumnoLogin(Resource):
    def post(self, alumno_id):
        request_data = request.get_json()
        
        if not request_data or 'password' not in request_data:
            abort(400, message='El cuerpo de la solicitud debe incluir la contraseña')

        password: str = request_data['password']
        
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        if not alumno:
            abort(404, message='No se encontró el alumno con la matrícula proporcionada')
        if alumno.password != password:
            abort(400, message='La contraseña es incorrecta')
            
        sessionString: str = random_string(128)
        
        put_item_to_dynamodb(
            getenv('DYNAMODB_TABLE_NAME'),
            {
                'id': {'S': str(uuid.uuid4())},  
                'fecha': {'N': str(int(time.time()))},
                'alumnoId': {'N': str(alumno_id)},
                'active': {'BOOL': True},  
                'sessionString': {'S': sessionString} 
            }
        )
        return Response(
            json.dumps({"sessionString": sessionString}),
            status=200,
            mimetype="application/json"
        )
        
class AlumnoVerifySession(Resource):
    def post(self, alumno_id):
        request_data = request.get_json()
        
        if not request_data or 'sessionString' not in request_data:
            abort(400, message='El cuerpo de la solicitud debe incluir la cadena de sesión')
        
        sessionString: str = request_data['sessionString']
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
            
        # función que recibe el nombre de la tabla y el filtro de búsqueda y regresa el resultado de la consulta
        response = scan_table(
            getenv('DYNAMODB_TABLE_NAME'),
            Attr('sessionString').eq(sessionString)
        )
        
        if response:
            is_active = response[0].get('active', False)
        if not response or not is_active:
            abort(400, message='Sesión no válida')
        
        return jsonify({
            "message": "Sesión verificada"
        })
        
class AlumnoLogout(Resource):
    def post(self, alumno_id):
        request_data = request.get_json()
        
        if not request_data or 'sessionString' not in request_data:
            abort(400, message='El cuerpo de la solicitud debe incluir la cadena de sesión')
        
        sessionString: str = request_data['sessionString']
        alumno = AlumnoModel.query.filter_by(id=alumno_id).first()
        
        if not alumno:
            abort(404, message='No se encontró el alumno con el ID proporcionado')
            
        response = scan_table(
            getenv('DYNAMODB_TABLE_NAME'),
            Attr('sessionString').eq(sessionString)
        )
        
        id = response[0].get('id', False)
        
        if not response or not id:
            abort(400, message='Sesión no válida')
            
        update_item_in_dynamodb(
            getenv('DYNAMODB_TABLE_NAME'),
            {'id': id},
            'SET active = :active' ,
            {':active': False}
        )
        
        return jsonify({
            "message": "Cierre de sesión exitoso"
        })