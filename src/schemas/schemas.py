from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


""" -------------------------------------------
CLIENTE
-------------------------------------------"""


class ClienteBase(BaseModel):
    nombre: str
    num_documento: str
    tipo_documento: str
    correo: bool
    telefono: int
    direccion: str
    id_banco: UUID


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    num_documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    correo: Optional[str] = None
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


""" -------------------------------------------
 USUARIO
 -------------------------------------------"""


class UsuarioBase(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    telefono: Optional[str] = None
    es_admin: bool = False


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    es_admin: Optional[bool] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    activo: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contraseña: str


class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str


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
