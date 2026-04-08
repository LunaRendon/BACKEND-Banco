from typing import List, Optional
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session, selectinload
from src.entities.Tarjeta import Tarjeta


class TarjetaCRUD:
    """
    Contiene las operaciones CRUD básicas para la entidad Tarjeta.
    """

    def __init__(self, db: Session):
        """Inicializa el CRUD con una sesión de base de datos."""
        self.db = db

    def crear_tarjeta(
        self,
        numero_tarjeta: str,
        tipo_tarjeta: str,
        fecha_vencimiento: date,
        cvv: str,
        estado: bool,
        id_cuenta: UUID,
    ) -> Tarjeta:
        """Crea una nueva tarjeta asociada a una cuenta.

        Se realizan validaciones mínimas de los campos y se verifica que la
        cuenta exista antes de persistir.
        """

        if not numero_tarjeta or len(numero_tarjeta) == 0:
            raise ValueError("El número de tarjeta es obligatorio")
        if len(numero_tarjeta) > 16:
            raise ValueError("El número de tarjeta no puede exceder 16 caracteres")

        if not tipo_tarjeta or len(tipo_tarjeta.strip()) == 0:
            raise ValueError("El tipo de tarjeta es obligatorio")

        if not fecha_vencimiento:
            raise ValueError("La fecha de vencimiento es obligatoria")

        if not cvv or len(cvv.strip()) == 0:
            raise ValueError("El CVV es obligatorio")
        if len(cvv) > 4:
            raise ValueError("El CVV no puede exceder 4 caracteres")

        if not estado:
            raise ValueError("El estado de la cuenta es obligatorio")

        from entities.Cuenta import Cuenta

        cuenta = self.db.query(Cuenta).filter(Cuenta.id_cuenta == id_cuenta).first()
        if not cuenta:
            raise ValueError("La cuenta especificada no existe")

        tarjeta = Tarjeta(
            numero_tarjeta=numero_tarjeta,
            tipo_tarjeta=tipo_tarjeta.strip(),
            fecha_vencimiento=fecha_vencimiento,
            cvv=cvv,
            estado=estado,
            id_cuenta=id_cuenta,
        )

        self.db.add(tarjeta)
        self.db.commit()
        self.db.refresh(tarjeta)
        return tarjeta

    def obtener_tarjeta(self, id_tarjeta: UUID, id_cuenta: UUID) -> Optional[Tarjeta]:
        """Devuelve una tarjeta por su id y la cuenta a la que pertenece."""
        return (
            self.db.query(Tarjeta)
            .filter(
                Tarjeta.id_tarjeta == id_tarjeta,
                Tarjeta.id_cuenta == id_cuenta,
            )
            .first()
        )

    def obtener_tarjetas(
        self, id_cuenta: UUID = None, skip: int = 0, limit: int = 100
    ) -> List[Tarjeta]:
        """Lista tarjetas, opcionalmente filtradas por cuenta."""
        query = self.db.query(Tarjeta).options(selectinload(Tarjeta.cuenta))
        if id_cuenta:
            query = query.filter(Tarjeta.id_cuenta == id_cuenta)
        return query.offset(skip).limit(limit).all()

    def obtener_tarjetas_por_numero(
        self, numero_tarjeta: str, id_cuenta: UUID
    ) -> List[Tarjeta]:
        return (
            self.db.query(Tarjeta)
            .filter(
                Tarjeta.numero_tarjeta == numero_tarjeta,
                Tarjeta.id_cuenta == id_cuenta,
            )
            .all()
        )

    def obtener_tarjetas_por_tipo(
        self, tipo_tarjeta: str, id_cuenta: UUID
    ) -> List[Tarjeta]:
        return (
            self.db.query(Tarjeta)
            .filter(
                Tarjeta.tipo_tarjeta == tipo_tarjeta,
                Tarjeta.id_cuenta == id_cuenta,
            )
            .all()
        )

    def obtener_tarjetas_por_estado(
        self, estado: bool, id_cuenta: UUID
    ) -> List[Tarjeta]:
        return (
            self.db.query(Tarjeta)
            .filter(
                Tarjeta.estado == estado,
                Tarjeta.id_cuenta == id_cuenta,
            )
            .all()
        )

    def actualizar_tarjeta(
        self, id_tarjeta: UUID, id_cuenta: UUID, **kwargs
    ) -> Optional[Tarjeta]:
        """Actualiza campos de una tarjeta existente."""

        tarjeta = self.obtener_tarjeta(id_tarjeta, id_cuenta)
        if not tarjeta:
            return None

        if "numero_tarjeta" in kwargs:
            numero = kwargs["numero_tarjeta"]
            if not numero or len(numero) == 0:
                raise ValueError("El número de tarjeta es obligatorio")
            if len(numero) > 16:
                raise ValueError("El número de tarjeta no puede exceder 16 caracteres")
            kwargs["numero_tarjeta"] = numero.strip()

        if "tipo_tarjeta" in kwargs:
            tipo = kwargs["tipo_tarjeta"]
            if not tipo or len(tipo.strip()) == 0:
                raise ValueError("El tipo de tarjeta es obligatorio")
            kwargs["tipo_tarjeta"] = tipo.strip()

        if "fecha_vencimiento" in kwargs:
            fecha = kwargs["fecha_vencimiento"]
            if not fecha:
                raise ValueError("La fecha de vencimiento es obligatoria")
            # asumimos que el valor ya es date

        if "cvv" in kwargs:
            cvv_val = kwargs["cvv"]
            if not cvv_val or len(cvv_val) == 0:
                raise ValueError("El CVV es obligatorio")
            if len(cvv_val) > 4:
                raise ValueError("El CVV no puede exceder 4 caracteres")
            kwargs["cvv"] = cvv_val.strip()

        if "estado" in kwargs:
            estado = kwargs["estado"]
            if not estado or len(estado) == 0:
                raise ValueError("El estado es obligatorio")
            kwargs["estado"] = estado

        for key, value in kwargs.items():
            if hasattr(tarjeta, key):
                setattr(tarjeta, key, value)

        self.db.commit()
        self.db.refresh(tarjeta)
        return tarjeta

    def actualizar_estado(
        self, id_tarjeta: UUID, estado: str, id_cuenta: UUID
    ) -> Optional[Tarjeta]:
        if not estado or len(estado) == 0:
            raise ValueError("El estado es obligatorio")
        if len(estado) > 20:
            raise ValueError("El estado no puede exceder 20 caracteres")
        return self.actualizar_tarjeta(id_tarjeta, id_cuenta=id_cuenta, estado=estado)

    def eliminar_tarjeta(self, id_tarjeta: UUID, id_cuenta: UUID) -> bool:
        tarjeta = self.obtener_tarjeta(id_tarjeta, id_cuenta)
        if tarjeta:
            self.db.delete(tarjeta)
            self.db.commit()
            return True
        return False
