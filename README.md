# Backend Banco — API REST

Backend de un sistema bancario desarrollado con **FastAPI**, **SQLAlchemy** y **PostgreSQL (Neon)**. Expone una API REST para gestionar bancos, clientes, cuentas, operaciones financieras y tarjetas, con autenticación de usuarios y menú interactivo por consola.

---
## Descripción

Este proyecto implementa el backend de un sistema bancario universitario. Permite registrar bancos, vincular clientes a ellos, gestionar cuentas de ahorro o corriente, realizar operaciones financieras (depósitos, retiros y transferencias) y administrar tarjetas débito/crédito.

El sistema cuenta con dos formas de interacción:
- **API REST** documentada con Swagger, accesible desde el navegador en `/docs`.
- **Menú por consola** que arranca la API en segundo plano y permite operar todas las entidades sin salir de la terminal.

---

## Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.11 | Lenguaje principal |
| FastAPI | 0.104.1 | Framework web y API REST |
| SQLAlchemy | 2.0.23 | ORM para la base de datos |
| Uvicorn | 0.24.0 | Servidor ASGI |
| PostgreSQL | — | Base de datos relacional |
| Neon | — | PostgreSQL en la nube (serverless) |
| Alembic | — | Migraciones de base de datos |
| python-dotenv | — | Gestión de variables de entorno |

---

## Estructura del proyecto

```
BACKEND-Banco/
├── main.py                  # Punto de entrada — menú por consola + API
├── alembic.ini              # Configuración de migraciones Alembic
├── requirements.txt         # Dependencias del proyecto
├── .env                     # Variables de entorno (no subir al repositorio)
├── init.db.py               # Script de inicialización de la base de datos
└── src/
    ├── auth/
    │   └── security.py      # Gestión de contraseñas (hash + verificación)
    ├── core/
    │   ├── exceptions.py    # Excepciones personalizadas
    │   ├── error_handlers.py# Manejadores globales de errores
    │   └── responses.py     # Modelos de respuesta estándar
    ├── crud/
    │   ├── Banco_crud.py    # Operaciones CRUD — Banco
    │   ├── Cliente_crud.py  # Operaciones CRUD — Cliente
    │   ├── Cuenta_crud.py   # Operaciones CRUD — Cuenta
    │   ├── Operacion_crud.py# Operaciones CRUD — Operación financiera
    │   ├── Tarjeta_crud.py  # Operaciones CRUD — Tarjeta
    │   ├── Usuario_crud.py  # Operaciones CRUD — Usuario administrador
    │   └── Usuario_App_crud.py # Operaciones CRUD — Usuario de la app
    ├── database/
    │   └── config.py        # Conexión SQLAlchemy + sesión + base declarativa
    ├── endpoints/
    │   ├── Banco.py         # Router FastAPI — /bancos
    │   ├── Cliente.py       # Router FastAPI — /clientes
    │   ├── Cuenta.py        # Router FastAPI — /cuentas
    │   ├── Operacion.py     # Router FastAPI — /operaciones
    │   ├── Tarjeta.py       # Router FastAPI — /tarjetas
    │   ├── Usuario.py       # Router FastAPI — /usuarios
    │   └── Uusuario_App.py  # Router FastAPI — /usuarios-app
    ├── entities/
    │   ├── Banco.py         # Modelo SQLAlchemy — tabla banco
    │   ├── Cliente.py       # Modelo SQLAlchemy — tabla cliente
    │   ├── Cuenta.py        # Modelo SQLAlchemy — tabla cuenta
    │   ├── Operacion.py     # Modelo SQLAlchemy — tabla operacion
    │   ├── Tarjeta.py       # Modelo SQLAlchemy — tabla tarjeta
    │   ├── Usuario.py       # Modelo SQLAlchemy — tabla usuario
    │   └── Usuario_App.py   # Modelo SQLAlchemy — tabla usuario_app
    ├── migrations/
    │   └── env.py           # Entorno de migraciones Alembic
    ├── schemas/
    │   ├── Banco_schema.py  # Pydantic — validación y serialización de Banco
    │   ├── Cliente_schema.py
    │   ├── Cuenta_schema.py
    │   ├── Operacion_schema.py
    │   ├── Tarjeta_schema.py
    │   ├── Usuario_schema.py
    │   ├── Usuario_App_schema.py
    │   └── schemas.py       # Esquema genérico de respuesta (RespuestaAPI)
    └── utils/
        └── app.py           # Instancia FastAPI + registro de routers y handlers
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

4. Crear el archivo `.env` en la raíz del proyecto con la URL de conexión:
```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db?sslmode=require
```

---

## Ejecución

### Opción 1 — Menú por consola (recomendado para pruebas)

Lanza la API en segundo plano e inicia el menú interactivo:

```bash
cd src
python ../main.py
```

El menú permite gestionar todas las entidades sin necesidad de un cliente HTTP:

```
========== MENÚ ==========
1. Bancos
2. Clientes
3. Cuentas
4. Operaciones
5. Tarjetas
6. Usuarios de la aplicación
7. Usuarios
0. Salir
```

### Opción 2 — Solo la API REST

```bash
cd src
uvicorn utils.app:app --reload --host 127.0.0.1 --port 8000
```

Acceder a la documentación interactiva:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Variables de entorno

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DATABASE_URL` | URL completa de conexión PostgreSQL | `postgresql://user:pass@host/db` |
| `DB_HOST` | Host de la base de datos (alternativo) | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL (alternativo) | `5432` |
| `DB_NAME` | Nombre de la base de datos (alternativo) | `neondb` |
| `DB_USERNAME` | Usuario de la base de datos (alternativo) | `postgres` |
| `DB_PASSWORD` | Contraseña de la base de datos (alternativo) | `••••••••` |

> Si se define `DATABASE_URL`, las variables individuales (`DB_HOST`, `DB_PORT`, etc.) son ignoradas.

---

## Migraciones

El proyecto usa **Alembic** para gestionar los cambios en el esquema de la base de datos.

Crear una nueva migración:
```bash
alembic revision --autogenerate -m "descripcion del cambio"
```

Aplicar migraciones pendientes:
```bash
alembic upgrade head
```

Revertir la última migración:
```bash
alembic downgrade -1
```

---

## Seguridad

Las contraseñas se almacenan usando **PBKDF2-HMAC-SHA256** con salt aleatorio de 32 bytes y 100.000 iteraciones. Nunca se guarda la contraseña en texto plano.

Requisitos de contraseña:
- Mínimo 8 caracteres, máximo 128
- Al menos una letra mayúscula
- Al menos una letra minúscula
- Al menos un número
- Al menos un carácter especial (`!@#$%^&*...`)

---

## Ramas del repositorio

| Rama | Descripción |
|---|---|
| `main` | Código estable de producción |
| `prod` | Rama de despliegue en producción |
| `dev` | Rama de desarrollo activo |
| `qa` | Rama de pruebas |

---

## Elaborado por
- Salomé Gil Chancí
- Luna Isabela Rendon Ramirez
- Carlos Eduardo Fajardo Suarez
