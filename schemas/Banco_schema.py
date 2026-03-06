from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

""" -------------------------------------------
    BANCO
    -------------------------------------------
-------------------------------------------"""


class BancoBase(BaseModel):
    nombre: str
    nit: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo_contacto: EmailStr


class BancoCreate(BancoBase):
    pass


class BancoUpdate(BaseModel):
    nombre: Optional[str] = None
    nit: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo_contacto: Optional[EmailStr] = None


class BancoResponse(BancoBase):
    id_banco: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True
