"Identidad Usuario_App"

import uuid
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base
from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    id_usuario: uuid, clave primaria
    username: nombre de usuario único para acceso a la app
    password_hash: contraseña cifrada del usuario
    fecha_registro: fecha y hora en la que se registró el usuario
    estado: estado del usuario (activo, inactivo, bloqueado)
    rol: rol del usuario (cliente, admin_app)
    id_cuenta: clave foránea de la entidad cuenta
"""


class Usuario_App(Base):
    __tablename__ = "usuarios_app"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    username = Column(String(50), unique=True, nullable=False)
    contraseña_hash = Column(String(255), nullable=False)
    fecha_registro = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    estado = Column(Boolean, default=False, nullable=True)
    rol = Column(String(20), nullable=False, default="cliente")

    id_cuenta = Column(
        UUID(as_uuid=True), ForeignKey("cuentas.id_cuenta"), nullable=True
    )

    cuenta = relationship("Cuenta", back_populates="usuario_app")

    def __repr__(self):
        return f"<Usuario_App(id_usuario={self.id_usuario}, username='{self.username}', rol='{self.rol}', estado='{self.estado}')>"
