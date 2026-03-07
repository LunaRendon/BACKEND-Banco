"""
Aplicación FastAPI. Ejecutar con:
  uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.config import create_tables
from endpoints import Cliente, Cuenta, Banco, Operacion, Tarjeta, Usuario, Uusuario_App

# Importar modelos para que Base.metadata los conozca
import entities.Banco  # noqa: F401 - registrar modelo
import entities.Cliente  # noqa: F401 - registrar modelo
import entities.Cuenta  # noqa: F401 - registrar modelo
import entities.Operacion  # noqa: F401 - registrar modelo
import entities.Tarjeta  # noqa: F401 - registrar modelo
import entities.Usuario  # noqa: F401 - registrar modelo
import entities.Usuario_App  # noqa: F401 - registrar modelo


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    # shutdown si hiciera falta


app = FastAPI(
    title="API completa",
    description="API con FastAPI, SQLAlchemy y PostgreSQL",
    lifespan=lifespan,
)

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
