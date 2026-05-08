from datetime import date
from uuid import UUID
from typing import List, Optional
from src.entities.Prestamos import Prestamos
from sqlalchemy.orm import Session, joinedload, selectinload


class PrestamoCRUD:
    """
    Clase para realizar operaciones CRUD sobre préstamos en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD con una sesión de base de datos.

        Args:
            db (Session): Sesión de SQLAlchemy para interactuar con la base de datos.
        """
        self.db = db

    def crear_prestamo(
        self,
        monto: float,
        interes: float,
        cuotas: int,
        estado: str,
        fecha_inicio: date,
        fecha_fin: date,
        id_cuenta: UUID,
        id_cliente: UUID,
        id_usuario_crea: UUID = None,
    ) -> Prestamos:
        """
        Crea un nuevo préstamo.

        Args:
            monto (float): Monto del préstamo.
            interes (float): Tasa de interés del préstamo.
            cuotas (int): Número de cuotas para el préstamo.
            estado (str): Estado del préstamo (por ejemplo, "Activo", "Pagado", "Vencido").
            fecha_inicio (date): Fecha en la que inicia el préstamo.
            fecha_fin (date): Fecha en la que debe devolverse el material.
            id_cuenta (UUID): Identificador único de la cuenta.
            id_cliente (UUID): Identificador único del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_crea (UUID, opcional): Usuario que registra el préstamo.

        Returns:
            Prestamo: Objeto de préstamo creado en la base de datos.
        """
        if not monto or monto <= 0:
            raise ValueError("El monto del préstamo debe ser un número positivo")
        if not interes or interes < 0:
            raise ValueError("La tasa de interés no puede ser negativa")
        if not cuotas or cuotas <= 0:
            raise ValueError("El número de cuotas debe ser un entero positivo")
        if not estado:
            raise ValueError("El estado del préstamo es obligatorio")
        if not fecha_inicio:
            raise ValueError("La fecha de inicio del préstamo es obligatoria")
        if not fecha_fin:
            raise ValueError("La fecha de fin del préstamo es obligatoria")
        if fecha_fin < fecha_inicio:
            raise ValueError(
                "La fecha de fin no puede ser anterior a la fecha de inicio"
            )
        if not id_cuenta:
            raise ValueError("La cuenta es obligatoria")
        if not id_cliente:
            raise ValueError("El cliente es obligatorio")
        if id_usuario_crea is None:
            raise ValueError("El usuario autenticado es obligatorio")

        prestamos = Prestamos(
            monto=monto,
            interes=interes,
            cuotas=cuotas,
            estado=estado,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            id_cuenta=id_cuenta,
            id_cliente=id_cliente,
            id_usuario_crea=id_usuario_crea,
        )

        self.db.add(prestamos)
        self.db.commit()
        self.db.refresh(prestamos)
        return prestamos

    def obtener_prestamo(
        self, id_prestamo: UUID, id_cliente: UUID
    ) -> Optional[Prestamos]:
        """
        Obtiene un préstamo específico.

        Args:
            id_prestamo (UUID): Identificador único del préstamo.
            id_cliente (UUID): Identificador único del cliente.

        Returns:
            Optional[Prestamos]: Préstamo encontrado o None si no existe.
        """
        return (
            self.db.query(Prestamos)
            .filter(
                Prestamos.id_prestamo == id_prestamo, Prestamos.id_cliente == id_cliente
            )
            .first()
        )

    def obtener_prestamos(
        self, id_cliente: UUID, skip: int = 0, limit: int = 100
    ) -> List[Prestamos]:
        return (
            self.db.query(Prestamos)
            .filter(Prestamos.id_cliente == id_cliente)
            .offset(skip)
            .limit(limit)
            .all()
        )

        """
        Obtiene préstamos realizados en una fecha específica.

        Args:
            fecha_inicio (date): Fecha de inicio del préstamo.
            id_cliente (UUID): Identificador único del cliente.

        Returns:
            List[Prestamos]: Lista de préstamos realizados en esa fecha.
        """
        return (
            self.db.query(Prestamos)
            .filter(
                Prestamos.fecha_inicio == fecha_inicio,
                Prestamos.id_cliente == id_cliente,
            )
            .all()
        )

    def obtener_prestamos_por_fecha_inicio(
        self, fecha_inicio: date, id_cliente: UUID
    ) -> List[Prestamos]:
        """
        Obtiene préstamos cuya fecha de fin coincide con la indicada.

        Args:
            fecha_fin (date): Fecha de fin del préstamo.
            id_cliente (UUID): Identificador único del cliente.

        Returns:
            List[Prestamos]: Lista de préstamos que cumplen con la fecha de fin.
        """

    def obtener_prestamos_por_fecha_fin(
        self, fecha_fin: date, id_cliente: UUID
    ) -> List[Prestamos]:

        return (
            self.db.query(Prestamos)
            .filter(
                Prestamos.fecha_fin == fecha_fin,
                Prestamos.id_cliente == id_cliente,
            )
            .all()
        )

    def obtener_prestamos_por_cliente(self, id_cliente: UUID) -> List[Prestamos]:
        """
        Obtiene los préstamos asociados a un cliente específico.

        Args:
            id_cliente (UUID): Identificador único del cliente.

        Returns:
            List[Prestamos]: Lista de préstamos del cliente.
        """
        return (
            self.db.query(Prestamos)
            .filter(
                Prestamos.id_cliente == id_cliente,
            )
            .all()
        )

    def actualizar_prestamo(
        self,
        id_prestamo: UUID,
        id_cliente: UUID,
        id_usuario_edita: UUID = None,
        **kwargs
    ) -> Optional[Prestamos]:
        """
        Actualiza los datos de un préstamo.

        Args:
            id_prestamo (UUID): Identificador único del préstamo.
            id_cliente (UUID): Identificador único del cliente.
            id_usuario_edita (UUID, opcional): Usuario que edita el préstamo.
            **kwargs: Campos a actualizar (fecha_prestamo, fecha_entrega, id_material, cod_cliente, etc.).

        Returns:
            Optional[Prestamos]: Préstamo actualizado o None si no existe.
        """
        prestamos = self.obtener_prestamo(id_prestamo, id_cliente)
        if not prestamos:
            return None

        if id_usuario_edita is None:
            raise ValueError("El usuario autenticado es obligatorio")

        prestamos.id_usuario_edita = id_usuario_edita

        if "fecha_inicio" in kwargs and kwargs["fecha_inicio"] is not None:
            fecha_inicio = kwargs["fecha_inicio"]
            if not isinstance(fecha_inicio, date):
                raise ValueError("La fecha de inicio debe ser un objeto date")
            prestamos.fecha_inicio = fecha_inicio

        if "fecha_fin" in kwargs and kwargs["fecha_fin"] is not None:
            fecha_fin = kwargs["fecha_fin"]
            if not isinstance(fecha_fin, date):
                raise ValueError("La fecha de fin debe ser un objeto date")
            prestamos.fecha_fin = fecha_fin

        if "id_cuenta" in kwargs and kwargs["id_cuenta"] is not None:
            prestamos.id_cuenta = kwargs["id_cuenta"]

        if "id_cliente" in kwargs and kwargs["id_cliente"] is not None:
            prestamos.id_cliente = kwargs["id_cliente"]

        for key, value in kwargs.items():
            if hasattr(prestamos, key):
                setattr(prestamos, key, value)

        self.db.commit()
        self.db.refresh(prestamos)
        return prestamos

    def actualizar_fecha_entrega(
        self,
        id_prestamo: UUID,
        id_cliente: UUID,
        nueva_fecha: date,
        id_usuario_edita: UUID = None,
    ) -> Optional[Prestamos]:
        """
        Actualiza únicamente la fecha de entrega de un préstamo.

        Args:
            id_prestamo (UUID): Identificador único del préstamo.
            id_cliente (UUID): Identificador único del cliente.
            nueva_fecha (date): Nueva fecha de entrega.
            id_usuario_edita (UUID, opcional): Usuario que edita el préstamo.

        Returns:
            Optional[Prestamos]: Préstamo actualizado o None si no existe.
        """
        if not isinstance(nueva_fecha, date):
            raise ValueError("La nueva fecha de entrega debe ser un objeto date")
        return self.actualizar_prestamo(
            id_prestamo,
            id_cliente=id_cliente,
            id_usuario_edita=id_usuario_edita,
            fecha_entrega=nueva_fecha,
        )

    def eliminar_prestamo(self, id_prestamo: UUID, id_cliente: UUID) -> bool:
        """
        Elimina un préstamo de la base de datos.

        Args:
            id_prestamo (UUID): Identificador único del préstamo.
            id_cliente (UUID): Identificador único del cliente.

        Returns:
            bool: True si se eliminó correctamente, False si no existe.
        """
        prestamos = self.obtener_prestamo(id_prestamo, id_cliente)
        if prestamos:
            self.db.delete(prestamos)
            self.db.commit()
            return True
        return False

    def obtener_todos_prestamos(
        self, skip: int = 0, limit: int = 100
    ) -> List[Prestamos]:
        return self.db.query(Prestamos).offset(skip).limit(limit).all()
