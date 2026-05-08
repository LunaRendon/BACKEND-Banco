import uuid
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base
from sqlalchemy import Column, ForeignKey, String, Float, Integer, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Prestamos(Base):

    __tablename__ = "prestamos"

    id_prestamo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    monto = Column(Float, nullable=False)
    interes = Column(Float, nullable=False)
    cuotas = Column(Integer, nullable=False)
    estado = Column(String(50), default="Activo")
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_cliente = Column(UUID(as_uuid=True), ForeignKey("clientes.id_cliente"))
    id_cuenta = Column(UUID(as_uuid=True), ForeignKey("cuentas.id_cuenta"))

    cliente = relationship("Cliente", back_populates="prestamos")
    cuenta = relationship("Cuenta", back_populates="prestamos")
    operaciones = relationship("Operacion", back_populates="prestamo")
