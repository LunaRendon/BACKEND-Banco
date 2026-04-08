"""IDENTIDAD OPERACION"""

import uuid
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


"""
ATRIBUTOS DE LA ENTIDAD:
    id_operacion: uuid, clave primaria
    tipo_operacion: tipo de operacion (deposito, retiro, transferencia)
    monto: valor monetario de la operacion
    fecha: fecha de la operacion
    id_cuenta_origen: clave foranea de la cuenta origen
    id_cuenta_destino: clave foranea de la cuenta destino
"""


class Operacion(Base):
    __tablename__ = "operaciones"

    id_operacion = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    tipo_operacion = Column(String(50), nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    id_cuenta_origen = Column(
        UUID(as_uuid=True), ForeignKey("cuentas.id_cuenta"), nullable=True
    )

    id_cuenta_destino = Column(
        UUID(as_uuid=True), ForeignKey("cuentas.id_cuenta"), nullable=True
    )

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    cuenta_origen = relationship(
        "Cuenta",
        foreign_keys=[id_cuenta_origen],
        back_populates="operaciones_origen",
    )

    cuenta_destino = relationship(
        "Cuenta",
        foreign_keys=[id_cuenta_destino],
        back_populates="operaciones_destino",
    )

    def __repr__(self):
        return f"<Operacion(id_operacion={self.id_operacion}, tipo_operacion='{self.tipo_operacion}', monto={self.monto})>"
