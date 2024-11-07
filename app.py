from flask import Flask
from flask_restful import Api

from resources.alumnos import Alumnos
from resources.alumnos import Alumno
from resources.profesores import Profesores
from resources.profesores import Profesor

app = Flask(__name__)
api = Api(app)

# Register API resources
api.add_resource(Alumnos, '/alumnos')
api.add_resource(Alumno, '/alumnos/<int:alumno_id>')
api.add_resource(Profesores, '/profesores')
api.add_resource(Profesor, '/profesores/<int:profesor_id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)
