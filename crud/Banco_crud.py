from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.Banco import Banco


class BancoCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_banco(
        self,
        nombre: str,
        nit: str,
        direccion: str,
        telefono: str,
        correo_contacto: str,
    ) -> Banco:

        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del banco es obligatorio")

        if not nit or len(nit.strip()) == 0:
            raise ValueError("El NIT es obligatorio")

        if not correo_contacto or len(correo_contacto.strip()) == 0:
            raise ValueError("El correo de contacto es obligatorio")

        banco = Banco(
            nombre=nombre.strip(),
            nit=nit.strip(),
            direccion=direccion.strip() if direccion else None,
            telefono=telefono.strip() if telefono else None,
            correo_contacto=correo_contacto.strip(),
        )

        self.db.add(banco)
        self.db.commit()
        self.db.refresh(banco)
        return banco

    def obtener_banco(self, id_banco: UUID) -> Optional[Banco]:
        return self.db.query(Banco).filter(Banco.id_banco == id_banco).first()

    def obtener_bancos(self, skip: int = 0, limit: int = 100) -> List[Banco]:
        return self.db.query(Banco).offset(skip).limit(limit).all()

    def actualizar_banco(self, id_banco: UUID, **kwargs) -> Optional[Banco]:
        banco = self.obtener_banco(id_banco)
        if not banco:
            return None

        for key, value in kwargs.items():
            if hasattr(banco, key) and value is not None:
                setattr(banco, key, value.strip() if isinstance(value, str) else value)

        self.db.commit()
        self.db.refresh(banco)
        return banco

    def eliminar_banco(self, id_banco: UUID) -> bool:
        banco = self.obtener_banco(id_banco)
        if banco:
            self.db.delete(banco)
            self.db.commit()
            return True
        return False