from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

""" -------------------------------------------
CLIENTE
-------------------------------------------"""


class ClienteBase(BaseModel):
    nombre: Optional[str] = None
    num_documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    correo: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    id_banco: UUID


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    num_documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    id_banco: Optional[UUID] = None


class BancoSimpleResponse(BaseModel):
    id_banco: UUID
    nombre: str


class ClienteResponse(ClienteBase):
    id_cliente: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    banco: Optional[BancoSimpleResponse] = None

    class Config:
        from_attributes = True
