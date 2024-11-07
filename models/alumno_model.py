class AlumnoModel:
    def __init__(self, id, nombres, apellidos, matricula, promedio):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.matricula = matricula
        self.promedio = promedio
        
    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        return self
