from flask import Flask
from flask_restful import Api
from flask_uploads import UploadSet, configure_uploads, IMAGES

from config import Config
from database import db
from resources.alumnos import Alumnos, Alumno, AlumnoFotoPerfil
from resources.profesores import Profesores
from resources.profesores import Profesor

app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(Config)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads/photos'  # Set the upload destination

db.init_app(app)
api = Api(app)

# Configure Flask-Uploads
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Register API resources
api.add_resource(Alumnos, '/alumnos')
api.add_resource(Alumno, '/alumnos/<int:alumno_id>')
api.add_resource(AlumnoFotoPerfil, '/alumnos/<int:alumno_id>/fotoPerfil')
api.add_resource(Profesores, '/profesores')
api.add_resource(Profesor, '/profesores/<int:profesor_id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)
