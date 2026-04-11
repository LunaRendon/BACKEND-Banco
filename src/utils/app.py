"""
Aplicación FastAPI. Ejecutar con:
  uvicorn utils.app:app --reload --host 127.0.0.1 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.database.config import create_tables
from src.endpoints import (
    Cliente,
    Cuenta,
    Banco,
    Operacion,
    Tarjeta,
    Usuario,
    Uusuario_App,
    login,
)
from src.core.config import get_settings
from src.core.exceptions import AppException
from src.core.error_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

# Importar modelos para que Base.metadata los conozca
import src.entities.Banco  # noqa: F401
import src.entities.Cliente  # noqa: F401
import src.entities.Cuenta  # noqa: F401
import src.entities.Operacion  # noqa: F401
import src.entities.Tarjeta  # noqa: F401
import src.entities.Usuario  # noqa: F401
import src.entities.Usuario_App  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="API Banco",
    description="API con FastAPI, SQLAlchemy y PostgreSQL",
    lifespan=lifespan,
)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

"Registrar handlers globales de core "
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

"Routers de endpoints"
app.include_router(Cliente.router)
app.include_router(Cuenta.router)
app.include_router(Banco.router)
app.include_router(Operacion.router)
app.include_router(Tarjeta.router)
app.include_router(Uusuario_App.router)
app.include_router(Usuario.router)
app.include_router(login.router)


@app.get("/")
def inicio():
    return {"mensaje": "API Banco", "docs": "/docs"}
