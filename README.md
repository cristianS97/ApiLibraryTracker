# 📚 ApiLibraryTracker

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

Este es el backend de la aplicación BookTracker, desarrollado con FastAPI. Proporciona un sistema de gestión de libros y autenticación centralizado mediante JWT (JSON Web Tokens) con seguridad basada en roles.

## 🛠️ Tecnologías utilizadas

* FastAPI: Framework principal de alto rendimiento.
* SQLAlchemy: ORM para la gestión de la base de datos SQLite.
* BCrypt: Hashing de contraseñas (uso directo para evitar conflictos).
* Python-Jose: Generación y validación de tokens JWT.
* Pydantic: Validación de esquemas y auto-documentación.

## 📂 Estructura del Proyecto

```text
A1BookTracker/
├── db/                   # Capa de datos y persistencia
│   ├── database.py       # Configuración de SQLite y sesión
│   └── operations/       # Lógica CRUD (Create, Read, Update, Delete)
│       ├── user.py       # Operaciones de usuario
│       └── book.py       # Operaciones de libros
├── routers/              # Controladores de la API (Endpoints)
│   ├── users.py          # Autenticación y usuarios
│   └── books.py          # Gestión de catálogo de libros
├── auth.py               # Utilidades de seguridad (Bcrypt + JWT)
├── models.py             # Definición de tablas de la base de datos
├── schemas.py            # Modelos de datos y validación de Pydantic
├── main.py               # Punto de entrada y configuración de la App
└── docker-compose.yml    # Configuración para contenedores
```

## 🚀 Configuración y Ejecución

1. Crear un entorno virtual:
   python -m venv venv

2. Activar el entorno:
   .\venv\Scripts\activate

3. Instalar dependencias:
   pip install fastapi uvicorn sqlalchemy bcrypt python-jose[cryptography]

4. Ejecutar el servidor:
   fastapi dev main.py

## 🔐 Endpoints Disponibles

### Autenticación (Usuarios)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| ![POST](https://img.shields.io/badge/POST-blue) | /users/register | Registra un nuevo usuario. (409 si ya existe). |
| ![POST](https://img.shields.io/badge/POST-blue) | /users/login | Valida credenciales y retorna un JWT Bearer Token. |

### Gestión de Libros
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| ![POST](https://img.shields.io/badge/POST-blue) | /book/ | Registra un nuevo libro. Valida duplicados por título/autor. |
| ![GET](https://img.shields.io/badge/GET-green) | /book/ | Retorna todos los libros. Permite filtrar por autor usando query params (?author=nombre) |
| ![GET](https://img.shields.io/badge/GET-green) | /book/{id}/ | Retorna la información detallada de un libro específico por su ID. |
| ![PUT](https://img.shields.io/badge/PUT-orange) | /book/{id}/ | Actualiza los datos de un libro existente. Requiere el cuerpo completo del recurso. |
| ![DELETE](https://img.shields.io/badge/DELETE-red) | /book/{id}/ | Elimina de forma permanente un libro del sistema según su ID. |

## 💻 Notas para el Desarrollador Android

Para conectar el emulador a la API en Docker, usa la dirección:
http://10.0.2.2:8000
