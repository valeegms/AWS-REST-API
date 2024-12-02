from flask_restful import reqparse

from validation import validate_nombres, validate_matricula, validate_promedio, validate_numeroEmpleado, validate_apellidos, validate_horasClase, validate_password

# Request parsers for students and teachers
alumnos_post_args = reqparse.RequestParser()
alumnos_post_args.add_argument('nombres', type=validate_nombres, required=True, help="El nombre del alumno no puede estar vacío")
alumnos_post_args.add_argument('apellidos', type=validate_apellidos, required=True, help="Los apellidos del alumno no pueden estar vacíos")
alumnos_post_args.add_argument('matricula', type=validate_matricula, required=True, help="La matrícula del alumno no puede estar vacía")
alumnos_post_args.add_argument('promedio', type=validate_promedio, required=True, help="El promedio del alumno no puede estar vacío")
alumnos_post_args.add_argument('fotoPerfilUrl', type=str, required=False)
alumnos_post_args.add_argument('password', type=str, required=True, help="La contraseña del alumno no puede estar vacía")

profesores_post_args = reqparse.RequestParser()
profesores_post_args.add_argument('numeroEmpleado', type=validate_numeroEmpleado, required=True, help="El número de empleado del profesor no puede estar vacío")
profesores_post_args.add_argument('nombres', type=validate_nombres, required=True, help="El nombre del profesor no puede estar vacío")
profesores_post_args.add_argument('apellidos', type=validate_apellidos, required=True, help="Los apellidos del profesor no pueden estar vacíos")
profesores_post_args.add_argument('horasClase', type=validate_horasClase, required=True, help="Las horas de clase del profesor no pueden estar vacías")

# Request parser for updating students and teachers with PATCH
alumnos_patch_args = reqparse.RequestParser()
alumnos_patch_args.add_argument('nombres', type=validate_nombres)
alumnos_patch_args.add_argument('apellidos', type=validate_apellidos)
alumnos_patch_args.add_argument('matricula', type=validate_matricula)
alumnos_patch_args.add_argument('promedio', type=validate_promedio)
alumnos_patch_args.add_argument('fotoPerfilUrl', type=str)
alumnos_patch_args.add_argument('password', type=validate_password)

profesores_patch_args = reqparse.RequestParser()
profesores_patch_args.add_argument('numeroEmpleado', type=validate_numeroEmpleado)
profesores_patch_args.add_argument('nombres', type=validate_nombres)
profesores_patch_args.add_argument('apellidos', type=validate_apellidos)
profesores_patch_args.add_argument('horasClase', type=validate_horasClase)


