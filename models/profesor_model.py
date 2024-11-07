class ProfesorModel:
    def __init__(self, id, numeroEmpleado, nombres, apellidos, horasClase):
        self.id = id
        self.numeroEmpleado = numeroEmpleado
        self.nombres = nombres
        self.apellidos = apellidos
        self.horasClase = horasClase
        
    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        return self