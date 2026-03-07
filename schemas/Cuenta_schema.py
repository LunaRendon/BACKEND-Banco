from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

""" -------------------------------------------
 CUENTA
 -------------------------------------------
"""


class CuentaBase(BaseModel):
    numero_cuenta: str
    tipo_cuenta: str
    saldo: str
    fecha_apertura: date
    estado: str
    id_cliente: UUID


class CuentaCreate(CuentaBase):
    pass


class CuentaUpdate(BaseModel):
    numero_cuenta: Optional[str] = None
    tipo_cuenta: Optional[str] = None
    saldo: Optional[str] = None
    fecha_apertura: Optional[datetime] = None
    estado: Optional[str] = None
    id_cliente: Optional[UUID] = None


class ClienteSimpleResponse(BaseModel):
    id_cliente: UUID
    nombre: str


class BancoSimpleResponse(BaseModel):
    id_banco: UUID
    nombre: str


class CuentaResponse(CuentaBase):
    id_cuenta: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    cliente: Optional[ClienteSimpleResponse] = None
    banco: Optional[BancoSimpleResponse] = None

    class Config:
        from_attributes = True
