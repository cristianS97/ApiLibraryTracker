# ApiLibraryTracker

Este es el backend de la aplicación BookTracker, desarrollado con FastAPI. Proporciona un sistema de autenticación centralizado mediante JWT (JSON Web Tokens) y seguridad basada en roles.

## 🛠️ Tecnologías utilizadas

* FastAPI: Framework principal.
* SQLAlchemy: ORM para la base de datos (SQLite).
* BCrypt: Hashing de contraseñas de alta seguridad.
* Python-Jose: Gestión de tokens JWT.
* Pydantic: Validación de tipos y esquemas de datos.

## 📂 Estructura del Proyecto

```text
A1BookTracker/
├── db/                   # Capa de datos
│   ├── database.py       # Conexión y sesión de base de datos
│   └── operations/       # Funciones CRUD específicas
│       └── user.py       # Lógica de persistencia de usuarios
├── routers/              # Controladores de la API
│   └── users.py          # Rutas de Login y Registro
├── auth.py               # Lógica de seguridad (JWT + Bcrypt)
├── models.py             # Definición de tablas SQLAlchemy
├── schemas.py            # Modelos de validación Pydantic
├── main.py               # Punto de entrada de la aplicación
└── docker-compose.yml    # Orquestación para despliegue
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

- POST /users/register : Crea un nuevo usuario. Valida si el nombre de usuario ya existe (retorna 409).
- POST /users/login    : Valida credenciales y retorna un "access_token" de tipo Bearer.

## 📱 Notas para la Aplicación Android

Para conectar el emulador o un dispositivo físico a esta API:
1. Localiza tu IP local (usando 'ipconfig' en el CMD).
2. En Retrofit (Android), usa la URL: http://TU_IP_LOCAL:8000/
3. No uses '127.0.0.1' en Android, ya que se refiere al propio teléfono.