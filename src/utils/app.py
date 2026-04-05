"""
Aplicación FastAPI. Ejecutar con:
  uvicorn utils.app:app --reload --host 127.0.0.1 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from database.config import create_tables
from endpoints import Cliente, Cuenta, Banco, Operacion, Tarjeta, Usuario, Uusuario_App
from core.exceptions import AppException
from core.error_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

# Importar modelos para que Base.metadata los conozca
import entities.Banco  # noqa: F401
import entities.Cliente  # noqa: F401
import entities.Cuenta  # noqa: F401
import entities.Operacion  # noqa: F401
import entities.Tarjeta  # noqa: F401
import entities.Usuario  # noqa: F401
import entities.Usuario_App  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="API Banco",
    description="API con FastAPI, SQLAlchemy y PostgreSQL",
    lifespan=lifespan,
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


@app.get("/")
def inicio():
    return {"mensaje": "API Banco", "docs": "/docs"}
