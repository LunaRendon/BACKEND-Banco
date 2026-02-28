from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.Operacion import Operacion
from entities.Cuenta import Cuenta


class OperacionCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_operacion(
        self,
        tipo_operacion: str,
        monto: float,
        id_cuenta_origen: UUID = None,
        id_cuenta_destino: UUID = None,
    ) -> Operacion:

        if not tipo_operacion or len(tipo_operacion.strip()) == 0:
            raise ValueError("El tipo de operación es obligatorio")

        if monto is None or monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        cuenta_origen = None
        cuenta_destino = None

        if id_cuenta_origen:
            cuenta_origen = (
                self.db.query(Cuenta)
                .filter(Cuenta.id_cuenta == id_cuenta_origen)
                .first()
            )
            if not cuenta_origen:
                raise ValueError("La cuenta origen no existe")

        if id_cuenta_destino:
            cuenta_destino = (
                self.db.query(Cuenta)
                .filter(Cuenta.id_cuenta == id_cuenta_destino)
                .first()
            )
            if not cuenta_destino:
                raise ValueError("La cuenta destino no existe")

        # Lógica financiera básica
        if tipo_operacion.lower() == "retiro":
            if not cuenta_origen:
                raise ValueError("El retiro requiere cuenta origen")
            if cuenta_origen.saldo < monto:
                raise ValueError("Saldo insuficiente")
            cuenta_origen.saldo -= monto

        elif tipo_operacion.lower() == "deposito":
            if not cuenta_destino:
                raise ValueError("El deposito requiere cuenta destino")
            cuenta_destino.saldo += monto

        elif tipo_operacion.lower() == "transferencia":
            if not cuenta_origen or not cuenta_destino:
                raise ValueError("La transferencia requiere cuenta origen y destino")
            if cuenta_origen.saldo < monto:
                raise ValueError("Saldo insuficiente")
            cuenta_origen.saldo -= monto
            cuenta_destino.saldo += monto

        operacion = Operacion(
            tipo_operacion=tipo_operacion.strip(),
            monto=monto,
            id_cuenta_origen=id_cuenta_origen,
            id_cuenta_destino=id_cuenta_destino,
        )

        self.db.add(operacion)
        self.db.commit()
        self.db.refresh(operacion)
        return operacion

    def obtener_operacion(self, id_operacion: UUID) -> Optional[Operacion]:
        return (
            self.db.query(Operacion)
            .filter(Operacion.id_operacion == id_operacion)
            .first()
        )

    def obtener_operaciones(self, skip: int = 0, limit: int = 100) -> List[Operacion]:
        return self.db.query(Operacion).offset(skip).limit(limit).all()

    def eliminar_operacion(self, id_operacion: UUID) -> bool:
        operacion = self.obtener_operacion(id_operacion)
        if operacion:
            self.db.delete(operacion)
            self.db.commit()
            return True
        return False
