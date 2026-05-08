from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal


class PrestamoBase(BaseModel):
    monto: Decimal
    interes: Decimal
    cuotas: int
    estado: Optional[str] = "Activo"
    fecha_inicio: date
    fecha_fin: Optional[date] = None

    id_cliente: UUID
    id_cuenta: UUID


class PrestamoCreate(PrestamoBase):
    pass


class PrestamoUpdate(BaseModel):
    monto: Optional[Decimal] = None
    interes: Optional[Decimal] = None
    cuotas: Optional[int] = None
    estado: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    id_cuenta: Optional[UUID] = None


class PrestamoResponse(PrestamoBase):
    id_prestamo: UUID

    fecha_creacion: Optional[datetime]
    fecha_edicion: Optional[datetime]

    class Config:
        from_attributes = True
