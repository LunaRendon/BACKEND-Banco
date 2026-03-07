from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date, datetime


""" -------------------------------------------
 TARJETA
 -------------------------------------------"""


class TarjetaBase(BaseModel):
    numero_tarjeta: str
    tipo_tarjeta: str
    fecha_vencimiento: date
    estado: str
    id_cuenta: UUID


class TarjetaCreate(TarjetaBase):
    cvv: str


class TarjetaUpdate(BaseModel):
    numero_tarjeta: Optional[str] = None
    tipo_tarjeta: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    cvv: Optional[str] = None
    estado: Optional[str] = None
    id_cuenta: Optional[UUID] = None


class TarjetaResponse(TarjetaBase):
    id_tarjeta: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True
