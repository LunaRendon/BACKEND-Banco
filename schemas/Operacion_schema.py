from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from decimal import Decimal

""" -------------------------------------------
 OPERACION
 -------------------------------------------"""


class OperacionBase(BaseModel):
    tipo_operacion: str
    monto: Decimal
    id_cuenta_origen: Optional[UUID] = None
    id_cuenta_destino: Optional[UUID] = None


class OperacionCreate(OperacionBase):
    pass


class OperacionUpdate(BaseModel):
    tipo_operacion: Optional[str] = None
    monto: Optional[Decimal] = None
    id_cuenta_origen: Optional[UUID] = None
    id_cuenta_destino: Optional[UUID] = None


class OperacionResponse(OperacionBase):
    id_operacion: UUID
    fecha: datetime
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True
