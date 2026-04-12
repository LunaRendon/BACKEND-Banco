# Backend Banco — API REST

Backend de un sistema bancario desarrollado con FastAPI, SQLAlchemy y PostgreSQL (Neon). Expone una API REST para gestionar bancos, clientes, cuentas, operaciones financieras y tarjetas, con autenticación JWT y menú interactivo por consola.

## 🎥 Video(Entrega 2)

[![Ver demo](https://img.shields.io/badge/Ver%20Demo-Google%20Drive-blue?logo=googledrive)](https://drive.google.com/file/d/1RK-WKW7WKS-xGMXiHenS_TIHh8SfwvUW/view?usp=sharing)

## Descripción

Este proyecto implementa el backend de un sistema bancario universitario. Permite registrar bancos, vincular clientes a ellos, gestionar cuentas de ahorro o corriente, realizar operaciones financieras (depósitos, retiros y transferencias) y administrar tarjetas débito/crédito.

El sistema cuenta con dos formas de interacción:

- **API REST** documentada con Swagger, accesible desde el navegador en `/docs`.
- **Menú por consola** que arranca la API en segundo plano y permite operar todas las entidades sin salir de la terminal.

## Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.11 | Lenguaje principal |
| FastAPI | 0.104.1 | Framework web y API REST |
| SQLAlchemy | 2.0.23 | ORM para la base de datos |
| Uvicorn | 0.24.0 | Servidor ASGI |
| PostgreSQL | — | Base de datos relacional |
| Neon | — | PostgreSQL en la nube (serverless) |
| python-jose | 3.3.0 | Generación y validación de tokens JWT |
| bcrypt | 5.0.0 | Hash seguro de contraseñas |
| pydantic-settings | 2.1.0 | Configuración desde variables de entorno |
| python-dotenv | 1.0.0 | Gestión de variables de entorno |

---

## Estructura del proyecto

```

BACKEND-Banco/
├── main.py                      # Punto de entrada — menú por consola + API
├── alembic.ini                  # Configuración de migraciones Alembic
├── requirements.txt             # Dependencias del proyecto
├── .env                         # Variables de entorno (no subir al repositorio)
├── init.db.py                   # Script de inicialización de la base de datos
└── src/
├── core/
│   ├── auth.py              # JWT: generación, validación y dependencia get_current_user
│   ├── config.py            # Configuración centralizada (JWT, CORS) desde .env
│   ├── exceptions.py        # Excepciones personalizadas
│   ├── error_handlers.py    # Manejadores globales de errores
│   └── responses.py         # Modelos de respuesta estándar
├── crud/
│   ├── Banco_crud.py        # Operaciones CRUD — Banco
│   ├── Cliente_crud.py      # Operaciones CRUD — Cliente
│   ├── Cuenta_crud.py       # Operaciones CRUD — Cuenta
│   ├── Operacion_crud.py    # Operaciones CRUD — Operación financiera
│   ├── Tarjeta_crud.py      # Operaciones CRUD — Tarjeta
│   ├── Usuario_crud.py      # Operaciones CRUD — Usuario administrador
│   └── Usuario_App_crud.py  # Operaciones CRUD — Usuario de la app
├── database/
│   └── config.py            # Conexión SQLAlchemy + sesión + base declarativa
├── endpoints/
│   ├── Banco.py             # Router FastAPI — /bancos
│   ├── Cliente.py           # Router FastAPI — /clientes
│   ├── Cuenta.py            # Router FastAPI — /cuentas
│   ├── Login.py             # Router FastAPI — /usuarios_app/login
│   ├── Operacion.py         # Router FastAPI — /operaciones
│   ├── Tarjeta.py           # Router FastAPI — /tarjetas
│   ├── Usuario.py           # Router FastAPI — /usuarios
│   └── Uusuario_App.py      # Router FastAPI — /usuarios_app
├── entities/
│   ├── Banco.py             # Modelo SQLAlchemy — tabla banco
│   ├── Cliente.py           # Modelo SQLAlchemy — tabla cliente
│   ├── Cuenta.py            # Modelo SQLAlchemy — tabla cuenta
│   ├── Operacion.py         # Modelo SQLAlchemy — tabla operacion
│   ├── Tarjeta.py           # Modelo SQLAlchemy — tabla tarjeta
│   ├── Usuario.py           # Modelo SQLAlchemy — tabla usuario
│   └── Usuario_App.py       # Modelo SQLAlchemy — tabla usuario_app
├── migrations/
│   └── env.py               # Entorno de migraciones Alembic
├── schemas/
│   ├── Banco_schema.py      # Pydantic — validación y serialización de Banco
│   ├── Cliente_schema.py
│   ├── Cuenta_schema.py
│   ├── Operacion_schema.py
│   ├── Tarjeta_schema.py
│   ├── Usuario_schema.py
│   ├── Usuario_App_schema.py
│   └── schemas.py           # Esquema genérico de respuesta (RespuestaAPI)
└── utils/
├── app.py               # Instancia FastAPI + CORS + registro de routers
└── security.py          # Hash y verificación de contraseñas con bcrypt
```
---

## Instalación y configuración

### Requisitos previos
- Python 3.11 o superior
- pip
- Acceso a una base de datos PostgreSQL (local o Neon)

### Pasos

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd BACKEND-Banco
```

2. Crear y activar el entorno virtual:
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Crear el archivo `.env` en la raíz del proyecto:
```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db?sslmode=require
JWT_SECRET_KEY=tu-clave-secreta-aqui
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Ejecución

### Opción 1 — Menú por consola
```bash
python main.py
```

### Opción 2 — Solo la API REST
```bash
uvicorn src.utils.app:app --reload --host 127.0.0.1 --port 8000
```

Acceder a la documentación interactiva:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Seguridad

### Autenticación JWT
La API usa JSON Web Tokens (JWT) para proteger los endpoints. El flujo es:

1. El usuario hace `POST /usuarios_app/login` con sus credenciales.
2. La API verifica la contraseña con bcrypt y devuelve un token JWT.
3. El token se incluye en el header `Authorization: Bearer <token>` en cada petición.
4. Los endpoints protegidos validan el token automáticamente con `get_current_user`.

Los únicos endpoints públicos son:
- `POST /usuarios_app/` — registro de nuevo usuario
- `POST /usuarios_app/login` — obtener token JWT

### CORS
El middleware CORS controla qué frontends pueden hacer peticiones a la API. Los orígenes permitidos se configuran desde el `.env` con la variable `CORS_ORIGINS`.

### Contraseñas
Las contraseñas se almacenan usando **bcrypt**. Nunca se guarda la contraseña en texto plano.

### Roles
`Usuario_App` tiene un campo `rol` con dos valores posibles:
- `cliente` — usuario regular de la app bancaria
- `admin_app` — usuario con privilegios extendidos

## Variables de entorno

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DATABASE_URL` | URL completa de conexión PostgreSQL | `postgresql://user:pass@host/db` |
| `JWT_SECRET_KEY` | Clave secreta para firmar tokens JWT | `openssl rand -hex 32` |
| `JWT_ALGORITHM` | Algoritmo de firma JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token en minutos | `60` |
| `CORS_ORIGINS` | Orígenes permitidos separados por coma | `http://localhost:3000` |

## Migraciones

```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripcion del cambio"

# Aplicar migraciones pendientes
alembic upgrade head

# Revertir la última migración
alembic downgrade -1
```

## Ramas del repositorio

| Rama | Descripción |
|---|---|
| `main` | Código estable de producción |
| `prod` | Rama de despliegue en producción |
| `dev` | Rama de desarrollo activo |
| `qa` | Rama de pruebas |

## Elaborado por

- Salomé Gil Chancí
- Luna Isabela Rendon Ramirez
- Carlos Eduardo Fajardo Suarez
