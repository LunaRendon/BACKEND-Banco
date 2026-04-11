"""IDENTIDAD BANCO"""

import uuid
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


"""
ATRIBUTOS DE LA ENTIDAD:
    id_banco: uuid, clave primaria
    nombre: nombre del banco
    nit: numero de identificacion tributaria
    direccion: direccion del banco
    telefono: telefono del banco
    correo_contacto: correo electronico del banco
"""


class Banco(Base):
    __tablename__ = "banco"

    id_banco = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    nombre = Column(String(100), nullable=False)
    nit = Column(String(50), unique=True, index=True, nullable=False)
    direccion = Column(String(150), nullable=True)
    telefono = Column(String(50), nullable=True)
    correo_contacto = Column(String(150), unique=True, nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    clientes = relationship("Cliente", back_populates="banco")

    def __repr__(self):
        return f"<Banco(id_banco={self.id_banco}, nombre='{self.nombre}', nit='{self.nit}', correo_contacto='{self.correo_contacto}')>"
