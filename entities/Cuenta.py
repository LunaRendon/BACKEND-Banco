"""IDENTIDAD CUENTA"""

import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Column, ForeignKey, String, Boolean, DateTime, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    id_cuenta: uuid, clave primaria
    numero_cuenta: numero de la cuenta del cliente
    tipo_cuenta: si es corriente, ahorro
    saldo:saldo total de la cuenta del cliente
    fecha_apertura: fecha en la que abrio la cuenta
    estado: estado de la cuenta
    id_cliente: clave foranea de la entidad cliente"""


class Cuenta(Base):
    __tablename__ = "cuentas"

    id_cuenta = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    numero_cuenta = Column(String(80), nullable=True)
    tipo_cuenta = Column(String(80), nullable=True)
    saldo = Column(Numeric(12, 2), nullable=False, default=0)
    fecha_apertura = Column(Date, nullable=True)
    estado = Column(Boolean, default=False, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_cliente = Column(UUID(as_uuid=True), ForeignKey("clientes.id_cliente"))

    id_usuario_crea = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    cliente = relationship("Cliente", back_populates="cuentas")
    operacion = relationship("Operacion", back_populates="cuentas")
    tarjeta = relationship("tarjeta", back_populates="cuentas")

    usuario_crea = relationship(
        "Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita"
    )
    usuario_edita = relationship(
        "Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea"
    )

    def __repr__(self):
        return f"<Cuenta(id_cuenta={self.id_cuenta}, numero_cuenta='{self.numero_cuenta}', tipo_cuenta='{self.tipo_cuenta}', saldo='{self.saldo}', fecha_apertura={self.fecha_apertura},estado={self.estado})>"
