from database import db

class AlumnoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(100), unique=True, nullable=False)
    promedio = db.Column(db.Double, nullable=False)
    fotoPerfilUrl = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'Alumno {self.nombres}, {self.apellidos}, {self.matricula}, {self.promedio}, {self.fotoPerfilUrl}, {self.password}'