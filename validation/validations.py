import re

def validate_id(id):
    if not(id >= 0):
        raise ValueError("El ID debe ser un número positivo")
    return id

def validate_nombres(nombres):
    if not nombres:
        raise ValueError("El nombre no puede estar vacío")
    if not re.match(r"^[A-Za-z\s\-]+$", nombres):
        raise ValueError("El nombre debe contener solo letras, espacios y guiones")
    return nombres

def validate_apellidos(apellidos):
    if not apellidos:
        raise ValueError("Los apellidos no pueden estar vacíos")
    if not re.match(r"^[A-Za-z\s\-']+$", apellidos):
        raise ValueError("Los apellidos deben contener solo letras, espacios, guiones y/o apóstrofes")
    return apellidos

def validate_matricula(matricula):
    if not matricula:
        raise ValueError("La matrícula no puede estar vacía")
    if not re.match(r"^A\d+$", matricula):
        raise ValueError("La matrícula debe empezar con una A seguida de dígitos")
    return matricula

def validate_numeroEmpleado(numeroEmpleado):
    if not(numeroEmpleado >= 0):
        raise ValueError("El número de empleado debe ser un número positivo")
    return numeroEmpleado

def validate_promedio(promedio):
    if not (0 <= promedio <= 100):
        raise ValueError("El promedio debe estar entre 0 y 100")
    return promedio

def validate_horasClase(horasClase):
    if not (0 <= horasClase <= 50):
        raise ValueError("Las horas de clase deben estar entre 0 y 50")
    return horasClase
