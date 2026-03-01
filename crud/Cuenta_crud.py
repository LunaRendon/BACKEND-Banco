from typing import List, Optional
from uuid import UUID
from entities.Cuenta import Cuenta
from sqlalchemy.orm import Session, selectinload
from datetime import date


class CuentaCRUD:
    """
    Clase para realizar operaciones CRUD sobre cuentas en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD con una sesión de base de datos.

        :param db: Sesión de SQLAlchemy para interactuar con la base de datos.
        :type db: Session
        """
        self.db = db

    def crear_cuenta(
        self,
        numero_cuenta: int,
        tipo_cuenta: str,
        saldo: float,
        fecha_apertura: date,
        estado: str,
        id_cliente: UUID,
        id_usuario_crea: UUID = None,
    ) -> Cuenta:
        """
        Crea una nueva cuenta en la base de datos.

        Args:
        id_cuenta: uuid, clave primaria
        numero_cuenta: numero de la cuenta del cliente
        tipo_cuenta: si es corriente, ahorro
        saldo:saldo total de la cuenta del cliente
        fecha_apertura: fecha en la que abrio la cuenta
        estado: estado de la cuenta
        id_cliente: clave foranea de la entidad client
            id_usuario_crea (UUID, opcional): Usuario que crea el cliente.
                Si no se especifica, se asigna un administrador por defecto.

        Returns:
            Cuenta: Objeto de la cuenta creada.

        Raises:
            ValueError: Si algún campo obligatorio no cumple las validaciones.
        """

        if not numero_cuenta or len(numero_cuenta.strip()) == 0:
            raise ValueError("El numero de la cuenta del cliente es obligatorio")
        if len(numero_cuenta) > 150:
            raise ValueError("El numero no puede exceder 150 caracteres")

        if not tipo_cuenta or len(tipo_cuenta.strip()) == 0:
            raise ValueError("El tipo de la cuenta del cliente es obligatorio")

        if not saldo or len(saldo.strip()) == 0:
            raise ValueError("El saldo de la cuenta es obligatoria")

        if not fecha_apertura:
            raise ValueError("La fecha de la sanción es obligatoria")

        if not estado or len(estado.strip()) == 0:
            raise ValueError("El estado de la cuenta es obligatorio")

        from entities.Cliente import Cliente

        cliente = (
            self.db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        )
        if not cliente:
            raise ValueError("El cliente especificado no existe")

        if id_usuario_crea is None:
            from entities.Usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear la cuenta"
                )
            id_usuario_crea = admin.id_usuario

        cuenta = Cuenta(
            numero_cuenta=numero_cuenta.strip(),
            tipo_cuenta=tipo_cuenta.strip(),
            saldo=saldo.strip(),
            fecha_apertura=fecha_apertura.strip(),
            estado=estado.strip(),
            id_cliente=id_cliente,
            id_usuario_crea=id_usuario_crea,
        )

        self.db.add(cuenta)
        self.db.commit()
        self.db.refresh(cuenta)
        return cuenta

    def obtener_cuenta(self, id_cuenta: UUID, id_cliente: UUID) -> Optional[Cuenta]:
        """
        Obtiene una cuenta específica por su código y su cliente.

        Args:
            id_cuenta (UUID): Identificador único de la cuenta.
            id_cliente (UUID): Identificador único del cliente.

        Returns:
            Optional[Cuenta]: Cuenta encontrada o None si no existe.
        """
        return (
            self.db.query(Cuenta)
            .filter(Cuenta.id_cuenta == id_cuenta, Cuenta.id_cliente == id_cliente)
            .first()
        )

    def obtener_cuentas(
        self, id_cliente: UUID = None, skip: int = 0, limit: int = 100
    ) -> List[Cuenta]:
        query = self.db.query(Cuenta).options(selectinload(Cuenta.cliente))
        if id_cliente:
            query = query.filter(Cuenta.id_cliente == id_cliente)
        return query.offset(skip).limit(limit).all()

    def obtener_cuenta_por_numeroCuenta(
        self, numero_cuenta: int, id_cliente: UUID
    ) -> List[Cuenta]:
        """
        Busca cuentas por numero de cuenta

        Args:
            numero_cuenta (int): numero de la cuenta del cliente
           id_cliente(UUID): id del cliente asociado a la cuenta

        Returns:
            List[Cuenta]: Lista de cuentas con ese numero.
        """
        return (
            self.db.query(Cuenta)
            .filter(
                Cuenta.numero_cuenta == numero_cuenta, Cuenta.id_cliente == id_cliente
            )
            .all()
        )

    def obtener_cuentas_por_tipodCuentas(
        self, tipo_cuenta: str, id_cliente: UUID
    ) -> List[Cuenta]:
        """
        Busca cuentas por tipo de cuentas

        Args:
            tipo_cuenta(str):tipo de cuenta del cliente
            id_cliente(UUID): id del cliente asociado a la cuenta

        Returns:
            List[Cuenta]: Lista de cuentas que coinciden con ese tipo de cuenta
        """
        return (
            self.db.query(Cuenta)
            .filter(
                Cuenta.tipo_cuenta == tipo_cuenta,
                Cuenta.id_cliente == id_cliente,
            )
            .all()
        )

    def obtener_cuentas_por_saldo(self, saldo: float, id_cliente: UUID) -> List[Cuenta]:
        """
        Busca cuentas por el saldo disponible

        Args:
            saldo (float): saldo de la cuenta
          id_cliente(UUID): id del cliente asociado a la cuenta
        Returns:
            List[Cuenta]: Lista de cuentas que coinciden con el saldo
        """
        return (
            self.db.query(Cuenta)
            .filter(
                Cuenta.saldo == saldo,
                Cuenta.id_cliente == id_cliente,
            )
            .all()
        )

    def obtener_cuentas_por_FechaApertura(
        self, fecha_apertura: date, id_cliente: UUID
    ) -> List[Cuenta]:
        """
        Obtiene cuentas segun la fecha de su apertura
        Args:
           fecha_apertura(date): fecha en la que se registro la cuenta
           id_cliente(UUID): id del cliente asociado a la cuenta

        Returns:
            List[Cuenta]: Lista de cuentas segun la fecha
        """
        return (
            self.db.query(Cuenta)
            .filter(
                Cuenta.fecha_apertura == fecha_apertura, Cuenta.id_cliente == id_cliente
            )
            .all()
        )

    def obtener_cuentas_por_estado(self, estado: str, id_cliente: UUID) -> List[Cuenta]:
        """
        Obtiene cuentas según su estado.

        Args:
            testado(str):estado actual de la cuenta
            id_cliente(UUID): id del cliente aosciado a la cuenta
        Returns:
            List[Cuenta]: Lista de cuentas segun el estado"""
        return (
            self.db.query(Cuenta)
            .filter(Cuenta.estado == estado, Cuenta.id_cliente == id_cliente)
            .all()
        )

    def actualizar_cuenta(
        self, id_cuenta: UUID, id_cliente: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Cuenta]:
        """
        Actualiza los datos de una cluenta.

        Args:
           id_cuenta(UUID): id de la cuenta
            id_cliente (UUID): id del cliente sociado a la cuenta
            id_usuario_edita (UUID, opcional): Usuario que edita el cliente.
                Si no se especifica, se asigna un administrador por defecto.
            **kwargs: Campos a actualizar (ej. nombre, tipo_cliente, detalle_tipo, vetado).

        Returns:
            Optional[Cuenta]: Cuenta actualizada o None si no existe.

        Raises:
            ValueError: Si algún valor enviado es inválido.
        """

        cuenta = (
            self.db.query(Cuenta)
            .filter(Cuenta.id_cuenta == id_cuenta, Cuenta.id_cliente == id_cliente)
            .first()
        )

        if not cuenta:
            return None

        if "numero_cuenta" in kwargs:
            numero_cuenta = kwargs["numero_cuenta"]
            if not numero_cuenta or len(numero_cuenta.strip()) == 0:
                raise ValueError("El numero de la cuenta del cliente es obligatorio")
            if len(numero_cuenta) > 150:
                raise ValueError("El numero no puede exceder 150 caracteres")
            kwargs["numero_cuenta"] = numero_cuenta.strip()

        if "tipo_cuenta" in kwargs:
            tipo_cuenta = kwargs["tipo_cuenta"]
            if not tipo_cuenta or len(tipo_cuenta.strip()) == 0:
                raise ValueError("El tipo de la cuenta es obligatoria")
            kwargs["tipo_cuenta"] = tipo_cuenta.strip()

        if "saldo" in kwargs:
            saldo = kwargs["saldo"]
            if not saldo or len(saldo.strip()) == 0:
                raise ValueError("El saldo es obligatorio")
            kwargs["saldo"] = saldo.strip()

        if "fecha_apertura" in kwargs:
            fecha_apertura = kwargs["fecha_apertura"]
            if not fecha_apertura or len(fecha_apertura.strip()) == 0:
                raise ValueError("La fecha de apertura es obligatoria")
            kwargs["fecha_apertura"] = fecha_apertura.strip()

        if "estado" in kwargs:
            estado = kwargs["estado"]
            if not estado or len(estado.strip()) == 0:
                raise ValueError("El estado es obligatorio")
            kwargs["estado"] = estado.strip()

        if id_usuario_edita is None:
            from entities.Usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar el cliente"
                )
            id_usuario_edita = admin.id_usuario

        cuenta.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(cuenta, key):
                setattr(cuenta, key, value)

        self.db.commit()
        self.db.refresh(cuenta)
        return cuenta

    def actualizar_estado(
        self, id_cuenta: UUID, estado: str, id_cliente: UUID
    ) -> Optional[Cuenta]:
        """
        Actualiza solo el estado de la cuenta delc liente

        Args:
            id_cliente (UUID): Identificador único del cliente.
            estado (str): Nuevo estado de la cuenta
            id_cuenta (UUID): Identificador único de la cuenta.

        Returns:
            Optional[Cuenta]: Cuenat actualizado o None si no existe.

        Raises:
            ValueError: Si el estado es inválido.
        """

        if not estado or len(estado.strip()) == 0:
            raise ValueError("El estado es obligatorio")
        if len(estado) > 50:
            raise ValueError("El estado no puede exceder 50 caracteres")

        return self.actualizar_cuenta(
            id_cuenta, id_cliente == id_cliente, estado=estado
        )

    def eliminar_cuenta(self, id_cuenta: UUID, id_cliente: UUID) -> bool:
        """
        Elimina una cuenta por su ID y el ID del cliente.

        Args:
            id_cuenta(UUID): id de la cuenta
            id_cliente (UUID): Identificador único del cliente.


        Returns:
            bool: True si el cliente fue eliminado, False si no existe.
        """
        cuenta = self.obtener_cuenta(id_cuenta, id_cliente)
        if cuenta:
            self.db.delete(cuenta)
            self.db.commit()
            return True
        return False
