from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date, datetime

""" -------------------------------------------
 Usuario_App
 -------------------------------------------"""


class UsuarioAppBase(BaseModel):
    username: str
    estado: bool
    rol: str = "cliente"
    id_cuenta: Optional[UUID] = None


class UsuarioAppCreate(UsuarioAppBase):
    contraseña: str


class UsuarioAppUpdate(BaseModel):
    username: Optional[str] = None
    contraseña: Optional[str] = None
    estado: Optional[bool] = None
    rol: Optional[str] = None
    id_cuenta: Optional[UUID] = None


class UsuarioAppResponse(UsuarioAppBase):
    id_usuario: UUID
    fecha_registro: datetime

    class Config:
        from_attributes = True
