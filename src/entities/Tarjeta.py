"""Identidad Tarjeta"""

import uuid
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base
from sqlalchemy import Column, ForeignKey, String, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    id_tarjeta: uuid, clave primaria
    numero_tarjeta: número único de la tarjeta del cliente
    tipo_tarjeta: tipo de tarjeta (crédito o débito)
    fecha_vencimiento: fecha en la que vence la tarjeta
    cvv: código de seguridad de la tarjeta
    estado: estado de la tarjeta (activa, bloqueada, vencida)
    id_cuenta: clave foránea de la entidad cuenta
"""


class Tarjeta(Base):
    __tablename__ = "tarjetas"

    id_tarjeta = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    numero_tarjeta = Column(String(16), nullable=False, unique=True)
    tipo_tarjeta = Column(String(20), nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    cvv = Column(String(4), nullable=False)
    estado = Column(Boolean, default=True)

    id_cuenta = Column(UUID(as_uuid=True), ForeignKey("cuentas.id_cuenta"))

    cuenta = relationship("Cuenta", back_populates="tarjetas")

    def __repr__(self):
        return f"<Tarjeta(id_tarjeta={self.id_tarjeta}, numero_tarjeta='{self.numero_tarjeta}', tipo_tarjeta='{self.tipo_tarjeta}', fecha_vencimiento={self.fecha_vencimiento},estado='{self.estado}')>"
