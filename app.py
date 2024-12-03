from flask import Flask
from flask_restful import Api
from flask_uploads import UploadSet, configure_uploads, IMAGES

from config import Config
from database import db
from resources.alumnos import AlumnoLogin, AlumnoLogout, AlumnoSendEmail, AlumnoVerifySession, Alumnos, Alumno, AlumnoFotoPerfil
from resources.profesores import Profesores
from resources.profesores import Profesor

app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(Config)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads/photos'  # Set the upload destination
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30


db.init_app(app)
api = Api(app)

# Configure Flask-Uploads
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Register API resources
api.add_resource(Alumnos, '/alumnos')
api.add_resource(Alumno, '/alumnos/<int:alumno_id>')
api.add_resource(AlumnoFotoPerfil, '/alumnos/<int:alumno_id>/fotoPerfil')
api.add_resource(AlumnoSendEmail, '/alumnos/<int:alumno_id>/email')
api.add_resource(AlumnoLogin, '/alumnos/<int:alumno_id>/session/login')
api.add_resource(AlumnoVerifySession, '/alumnos/<int:alumno_id>/session/verify')
api.add_resource(AlumnoLogout, '/alumnos/<int:alumno_id>/session/logout')
api.add_resource(Profesores, '/profesores')
api.add_resource(Profesor, '/profesores/<int:profesor_id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)
