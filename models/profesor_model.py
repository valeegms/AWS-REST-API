from database import db

class ProfesorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    numeroEmpleado = db.Column(db.String(100), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    horasClase = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'Profesor {self.numeroEmpleado}, {self.nombres}, {self.apellidos}, {self.horasClase}'