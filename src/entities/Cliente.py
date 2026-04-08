"""IDENTIDAD CLIENTE"""

import uuid
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base
from sqlalchemy import Column, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    id_cliente: uuid, clave primaria
    nombre:nombre completo del cliente
    num_documento: numero del documento
    tipo_documento: que tipo de documento tiene si es: cedula, Cedula estranjera, Tarjeta identidad
    correo: correo electronico del cliente
    telefono: telefono del cliente
    direccion: direccion del cliente
    id_banco: clave foranea de la entidad banco"""


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(80), nullable=True)
    num_documento = Column(String(80), nullable=True)
    tipo_documento = Column(String(80), nullable=True)
    correo = Column(String(150), unique=True, index=True, nullable=False)
    telefono = Column(String(80), nullable=True)
    direccion = Column(String(150), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_banco = Column(UUID(as_uuid=True), ForeignKey("banco.id_banco"))

    id_usuario_crea = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    banco = relationship("Banco", back_populates="clientes")
    cuentas = relationship("Cuenta", back_populates="cliente")

    usuario_crea = relationship(
        "Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita"
    )
    usuario_edita = relationship(
        "Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea"
    )

    def __repr__(self):
        return f"<Cliente(id_cliente={self.id_cliente}, nombre='{self.nombre}', num_documento='{self.num_documento}', tipo_documento='{self.tipo_documento}', correo={self.correo},telefono={self.telefono},direccion={self.direccion})>"
