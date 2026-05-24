"""
Aplicación FastAPI. Ejecutar con:
  uvicorn src.utils.app:app --reload --host 127.0.0.1 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import Response

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
    Prestamos,
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
import src.entities.Prestamos  # noqa: F401


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


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response: Response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https://fastapi.tiangolo.com; "
        "frame-ancestors 'none'; "
        "base-uri 'self';"
    )

    return response


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
app.include_router(Prestamos.router)


@app.get("/")
def inicio():
    return {"success": True, "data": {"mensaje": "API Banco", "docs": "/docs"}}
