from typing import List, Optional
from uuid import UUID
from entities.Cliente import Cliente
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