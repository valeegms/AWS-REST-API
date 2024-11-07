# Flask REST API for Student and Teacher Management

RESTful API built with Flask for managing information about students (`Alumnos`) and teachers (`Profesores`). It allows users to perform CRUD operations on each entity.

- [Flask REST API for Student and Teacher Management](#flask-rest-api-for-student-and-teacher-management)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Setup and Installation (Windows)](#setup-and-installation-windows)
  - [API Endpoints](#api-endpoints)
    - [Alumno (Student) Endpoints](#alumno-student-endpoints)
    - [Profesor (Teacher) Endpoints](#profesor-teacher-endpoints)

---

## Features

- Create, Read, Update, and Delete (CRUD) operations for:
  - **Students** (`Alumnos`): Stores `id`, `nombres`, `apellidos`, `matricula`, and `promedio`.
  - **Teachers** (`Profesores`): Stores `id`, `numeroEmpleado`, `nombres`, `apellidos`, and `horasClase`.
- In-memory data storage for simplicity (data will reset when the server restarts).
- Modularized codebase for easier maintenance.
- Validation for each field to ensure proper data entry.

## Technologies Used

- **Python 3.8+**
- **Flask:** Web framework for building the REST API.
- **Flask-RESTful:** Extension for creating RESTful APIs.

## Setup and Installation (Windows)

1. **Clone the repository**
   ```bash
   git clone https://github.com/valeegms/REST-API.git
   cd REST-API
2. **Create and activate a virtual environment**
   ```powershell
   python -m .venv venv
   .venv\Scripts\Activate.ps1 #Windows
   ```
    > :memo: **Note:** It may be required to enable the `Activate.ps1` script by setting the execution policy for the user with the following PowerShell command:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run the project**
   ```powershell
   python api.py
   ```
   The app will run on `http://127.0.0.1:5000/` by default

## API Endpoints
### Alumno (Student) Endpoints
|  Method  |  Endpoint     |  Description              |
|----------|---------------|---------------------------|
|GET       |`/alumnos`     |Get all students           |
|GET       |`/alumnos/<id>`|Get a specific student     |
|POST      |`/alumnos`     |Add a new student          |
|PUT       |`/alumnos<id>` |Full update a new student  |
|PATCH     |`/alumnos<id>` |Partial update of a student|
|DELETE    |`/alumnos<id>` |Delete a student           |

### Profesor (Teacher) Endpoints
|  Method  |  Endpoint        |  Description              |
|----------|------------------|---------------------------|
|GET       |`/profesores`     |Get all teachers           |
|GET       |`/profesores/<id>`|Get a specific teacher     |
|POST      |`/profesores`     |Add a new teacher          |
|PUT       |`/profesores<id>` |Full update a new teacher  |
|PATCH     |`/profesores<id>` |Partial update of a teacher|
|DELETE    |`/profesores<id>` |Delete a teacher           |