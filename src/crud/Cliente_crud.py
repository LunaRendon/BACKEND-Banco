from typing import List, Optional
from uuid import UUID
from src.entities.Cliente import Cliente
from sqlalchemy.orm import Session, selectinload


class ClienteCRUD:
    """
    Clase para realizar operaciones CRUD sobre clientes en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD con una sesión de base de datos.

        :param db: Sesión de SQLAlchemy para interactuar con la base de datos.
        :type db: Session
        """
        self.db = db

    def crear_cliente(
        self,
        nombre: str,
        num_documento: str,
        tipo_documento: str,
        correo: str,
        telefono: str,
        direccion: str,
        id_banco: UUID,
        id_usuario_crea: UUID = None,
    ) -> Cliente:
        """
        Crea un nuevo cliente en la base de datos.

        Args:
            nombre (str): Nombre del cliente.
            num_documento (int): numero documento
            tipo_docuemnto (str): tipo de documento (cc,ti)
            correo(str): correo electronico
            telefono(int): telefono del cliente
            direccion(str): direccion del cliente
            id_banco: codigo unico del banco al q pertenece
            id_usuario_crea (UUID, opcional): Usuario que crea el cliente.
                Si no se especifica, se asigna un administrador por defecto.

        Returns:
            Cliente: Objeto del cliente creado.

        Raises:
            ValueError: Si algún campo obligatorio no cumple las validaciones.
        """

        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del cliente es obligatorio")
        if len(nombre) > 150:
            raise ValueError("El nombre no puede exceder 150 caracteres")

        if not num_documento or len(num_documento.strip()) == 0:
            raise ValueError("El documento del cliente es obligatorio")

        if not tipo_documento or len(tipo_documento.strip()) == 0:
            raise ValueError("El tipo de documento es obligatorio")

        if not correo or len(correo.strip()) == 0:
            raise ValueError("El correo es obligatorio")

        if not telefono or len(telefono.strip()) == 0:
            raise ValueError("El telefono es obligatorio")

        if not direccion or len(direccion.strip()) == 0:
            raise ValueError("La direccion es obligatoria")

        from entities.Banco import Banco

        banco = self.db.query(Banco).filter(Banco.id_banco == id_banco).first()
        if not banco:
            raise ValueError("El banco especificado no existe")

        if id_usuario_crea is None:
            from entities.Usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear el cliente"
                )
            id_usuario_crea = admin.id_usuario

        cliente = Cliente(
            nombre=nombre.strip(),
            num_documento=num_documento.strip(),
            tipo_documento=tipo_documento.strip(),
            correo=correo.strip(),
            telefono=telefono.strip(),
            direccion=direccion.strip(),
            id_banco=id_banco,
            id_usuario_crea=id_usuario_crea,
        )

        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def obtener_cliente(self, id_cliente: UUID, id_banco: UUID) -> Optional[Cliente]:
        """
        Obtiene un cliente específico por su código y su banco.

        Args:
            id_cliente (UUID): Identificador único del cliente.
            id_banco (UUID): Identificador único del banco.

        Returns:
            Optional[Cliente]: Cliente encontrado o None si no existe.
        """
        return (
            self.db.query(Cliente)
            .filter(Cliente.id_cliente == id_cliente, Cliente.id_banco == id_banco)
            .first()
        )

    def obtener_clientes(
        self, id_banco: UUID = None, skip: int = 0, limit: int = 100
    ) -> List[Cliente]:
        query = self.db.query(Cliente).options(selectinload(Cliente.banco))
        if id_banco:
            query = query.filter(Cliente.id_banco == id_banco)
        return query.offset(skip).limit(limit).all()

    def obtener_clientes_por_nombre(self, nombre: str, id_banco: UUID) -> List[Cliente]:
        """
        Busca clientes por nombre en el banco.

        Args:
            nombre (str): Nombre del cliente.
            id_banco (UUID): Identificador único del banco.

        Returns:
            List[Cliente]: Lista de clientes con ese nombre.
        """
        return (
            self.db.query(Cliente)
            .filter(Cliente.nombre == nombre, Cliente.id_banco == id_banco)
            .all()
        )

    def obtener_clientes_por_numeroDocumento(
        self, num_documento: str, id_banco: UUID
    ) -> List[Cliente]:
        """
        Busca clientes por numero de docuemnto en el banco.

        Args:
            num_documento (str): numero de documento del cliente
            id_banco (UUID): Identificador único del banco.

        Returns:
            List[Cliente]: Lista de clientes que coinciden con ese numero de documento.
        """
        return (
            self.db.query(Cliente)
            .filter(
                Cliente.num_documento == str(num_documento),
                Cliente.id_banco == id_banco,
            )
            .all()
        )

    def obtener_clientes_por_tipoDocumento(
        self, tipo_documento: str, id_banco: UUID
    ) -> List[Cliente]:
        """
        Busca clientes por el tipo de documento en el banco

        Args:
            tipo_documento (str): tipo del documento del cliente
            id_banco (UUID): Identificador único del banco.

        Returns:
            List[Cliente]: Lista de clientes que coinciden con ese tipo de documento.
        """
        return (
            self.db.query(Cliente)
            .filter(
                Cliente.tipo_documento == tipo_documento,
                Cliente.id_banco == id_banco,
            )
            .all()
        )

    def obtener_clientes_por_correo(self, correo: str, id_banco: UUID) -> List[Cliente]:
        """
        Obtiene clientes según su correo.

        Args:
            correo (str): correo del cliente
            id_banco (UUID): Identificador único del banco.

        Returns:
            List[Cliente]: Lista de clientes segun el correo
        """
        return (
            self.db.query(Cliente)
            .filter(Cliente.correo == correo, Cliente.id_banco == id_banco)
            .all()
        )

    def obtener_clientes_por_telefono(
        self, telefono: str, id_banco: UUID
    ) -> List[Cliente]:
        """
        Obtiene clientes según su telefono.

        Args:
            telefono (str): telefono del cliente
            id_banco (UUID): Identificador único del banco.

        Returns:
            List[Cliente]: Lista de clientes segun el telefono
        """
        return (
            self.db.query(Cliente)
            .filter(Cliente.telefono == telefono, Cliente.id_banco == id_banco)
            .all()
        )

    def obtener_clientes_por_direccion(
        self, direccion: str, id_banco: UUID
    ) -> List[Cliente]:
        """
        Obtiene clientes según su direccion.

        Args:
            direccion (str): direccion del cliente
            id_banco (UUID): Identificador único del banco.

        Returns:
            List[Cliente]: Lista de clientes segun la direccion
        """
        return (
            self.db.query(Cliente)
            .filter(Cliente.direccion == direccion, Cliente.id_banco == id_banco)
            .all()
        )

    def actualizar_cliente(
        self, id_cliente: UUID, id_banco: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Cliente]:
        """
        Actualiza los datos de un cliente.

        Args:
            id_cliente (UUID): Identificador único del cliente.
            id_banco (UUID): Identificador único del banco.
            id_usuario_edita (UUID, opcional): Usuario que edita el cliente.
                Si no se especifica, se asigna un administrador por defecto.
            **kwargs: Campos a actualizar (ej. nombre, tipo_cliente, detalle_tipo, vetado).

        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe.

        Raises:
            ValueError: Si algún valor enviado es inválido.
        """

        cliente = (
            self.db.query(Cliente)
            .filter(Cliente.id_cliente == id_cliente, Cliente.id_banco == id_banco)
            .first()
        )

        if not cliente:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre del cliente es obligatorio")
            if len(nombre) > 150:
                raise ValueError("El nombre no puede exceder 150 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "num_documento" in kwargs:
            num_doc = kwargs["num_documento"]
            if not num_doc or len(num_doc.strip()) == 0:
                raise ValueError("El numero de documento del cliente es obligatorio")
            kwargs["num_documento"] = num_doc.strip()

        if "tipo_documento" in kwargs:
            tipo_doc = kwargs["tipo_documento"]
            if not tipo_doc or len(tipo_doc.strip()) == 0:
                raise ValueError("El tipo de documento es obligatorio")
            kwargs["tipo_documento"] = tipo_doc.strip()

        if "correo" in kwargs:
            correo = kwargs["correo"]
            if not correo or len(correo.strip()) == 0:
                raise ValueError("El correo es obligatorio")
            kwargs["correo"] = correo.strip()

        if "telefono" in kwargs:
            telefono = kwargs["telefono"]
            if not telefono or len(telefono.strip()) == 0:
                raise ValueError("El telefono es obligatorio")
            kwargs["telefono"] = telefono.strip()

        if "direccion" in kwargs:
            direccion = kwargs["direccion"]
            if not direccion or len(direccion.strip()) == 0:
                raise ValueError("La direccion obligatoria")
            kwargs["direccion"] = direccion.strip()

        if id_usuario_edita is None:
            from entities.Usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar el cliente"
                )
            id_usuario_edita = admin.id_usuario

        cliente.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(cliente, key):
                setattr(cliente, key, value)

        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def actualizar_tipoDocumento(
        self, id_cliente: UUID, tipo_documento: str, id_banco: UUID
    ) -> Optional[Cliente]:
        """
        Actualiza solo el tipo de documento de un cliente.

        Args:
            id_cliente (UUID): Identificador único del cliente.
            tipo_documento (str): Nuevo tipo de documento del cliente.
            id_biblioteca (UUID): Identificador único del banco.

        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe.

        Raises:
            ValueError: Si el tipo de documento es inválido.
        """

        if not tipo_documento or len(tipo_documento.strip()) == 0:
            raise ValueError("El tipo de documento es obligatorio")
        if len(tipo_documento) > 50:
            raise ValueError("El tipo de documento no puede exceder 50 caracteres")

        return self.actualizar_cliente(
            id_cliente, id_banco=id_banco, tipo_documento=tipo_documento
        )

    def actualizar_telefono(
        self, id_cliente: UUID, telefono: str, id_banco: UUID
    ) -> Optional[Cliente]:
        """
        Actualiza solo el telefono de un cliente.

        Args:
            id_cliente (UUID): Identificador único del cliente.
            telefono (str): Nuevo telefono del cliente.
            id_biblioteca (UUID): Identificador único del banco.

        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe.

        Raises:
            ValueError: Si el detalle excede el límite permitido.
        """
        if telefono and len(telefono.strip()) > 100:
            raise ValueError("El telefono no puede exceder 100 caracteres")

        return self.actualizar_cliente(id_cliente, id_banco=id_banco, telefono=telefono)

    def actualizar_correo(
        self, id_cliente: UUID, correo: str, id_banco: UUID
    ) -> Optional[Cliente]:
        """
        Actualiza el correo de un cliente

        Args:
            id_cliente (UUID): Identificador único del cliente.
           correo(str): nuevo correo del cliente
            id_biblioteca (UUID): Identificador único del banco.

        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe.
        """
        return self.actualizar_cliente(id_cliente, id_banco=id_banco, correo=correo)

    def actualizar_direccion(
        self, id_cliente: UUID, direccion: str, id_banco: UUID
    ) -> Optional[Cliente]:
        """
        Actualiza la direccion de un cliente

        Args:
            id_cliente (UUID): Identificador único del cliente.
           direccion(str): nueva direccion del cliente
            id_banco (UUID): Identificador único del banco.

        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe.
        """
        return self.actualizar_cliente(
            id_cliente, id_banco=id_banco, direccion=direccion
        )

    def eliminar_cliente(self, id_cliente: UUID, id_banco: UUID) -> bool:
        """
        Elimina un cliente por su ID y banco.

        Args:
            id_cliente (UUID): Identificador único del cliente.
            id_banco (UUID): Identificador único del banco.

        Returns:
            bool: True si el cliente fue eliminado, False si no existe.
        """
        cliente = self.obtener_cliente(id_cliente, id_banco)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False
