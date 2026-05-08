from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, selectinload
from src.entities.Usuario_App import Usuario_App
from src.utils.security import hash_password


class UsuarioAppCRUD:
    """
    Contiene las operaciones CRUD básicas para la entidad Usuario_App.
    """

    def __init__(self, db: Session):
        """Inicializa el CRUD con una sesión de base de datos."""
        self.db = db

    def crear_usuario(
        self,
        username: str,
        contraseña: str,
        estado: bool,
        id_cuenta: UUID,
        rol: str = "cliente",
    ) -> Usuario_App:
        """
        Crea un nuevo usuario de la app.

        Se realizan validaciones básicas y se verifica
        que la cuenta exista.
        """

        if not username or len(username.strip()) == 0:
            raise ValueError("El username es obligatorio")
        if len(username) > 50:
            raise ValueError("El username no puede exceder 50 caracteres")

        if not contraseña or len(contraseña.strip()) == 0:
            raise ValueError("La contraseña es obligatoria")
        if len(contraseña) > 255:
            raise ValueError("La contraseña no puede exceder 255 caracteres")

        if not estado:
            raise ValueError("El estado es obligatorio")

        if id_cuenta:
            from src.entities.Cuenta import Cuenta

            cuenta = self.db.query(Cuenta).filter(Cuenta.id_cuenta == id_cuenta).first()
        if not cuenta:
            raise ValueError("La cuenta especificada no existe")

        usuario_existente = (
            self.db.query(Usuario_App)
            .filter(Usuario_App.id_cuenta == id_cuenta)
            .first()
        )
        if usuario_existente:
            raise ValueError("Esta cuenta bancaria ya tiene un usuario registrado")

        usuario = Usuario_App(
            username=username.strip(),
            contraseña_hash=hash_password(contraseña),
            estado=estado,
            rol=rol,
            id_cuenta=id_cuenta,
        )

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, id_usuario: UUID) -> Optional[Usuario_App]:
        """Obtiene un usuario por su id."""
        return (
            self.db.query(Usuario_App)
            .options(selectinload(Usuario_App.cuenta))
            .filter(Usuario_App.id_usuario == id_usuario)
            .first()
        )

    def obtener_usuariosApp(self, skip: int = 0, limit: int = 100) -> List[Usuario_App]:
        return self.db.query(Usuario_App).offset(skip).limit(limit).all()

    def obtener_usuario_por_username(self, username: str) -> Optional[Usuario_App]:
        """Obtiene un usuario por username."""
        return (
            self.db.query(Usuario_App).filter(Usuario_App.username == username).first()
        )

    def obtener_usuarios_por_estado(self, estado: bool) -> List[Usuario_App]:
        """Obtiene usuarios por estado."""
        return self.db.query(Usuario_App).filter(Usuario_App.estado == estado).all()

    def actualizar_usuario(self, id_usuario: UUID, **kwargs) -> Optional[Usuario_App]:
        """
        Actualiza los datos de un usuario.
        """

        usuario = self.obtener_usuario(id_usuario)

        if not usuario:
            return None

        if "username" in kwargs:
            username = kwargs["username"]

            if not username or len(username.strip()) == 0:
                raise ValueError("El username es obligatorio")

            if len(username) > 50:
                raise ValueError("El username no puede exceder 50 caracteres")

            kwargs["username"] = username.strip()

        if "contraseña" in kwargs:
            password = kwargs["contraseña"]

            if not password or len(password.strip()) == 0:
                raise ValueError("La contraseña es obligatoria")

            if len(password) > 255:
                raise ValueError("La contraseña no puede exceder 255 caracteres")

            kwargs["contraseña_hash"] = hash_password(password.strip())
            del kwargs["contraseña"]

        if "estado" in kwargs:
            estado = kwargs["estado"]
            if not estado or len(estado) == 0:
                raise ValueError("El estado es obligatorio")
            kwargs["estado"] = estado

        if "id_cuenta" in kwargs:
            id_cuenta = kwargs["id_cuenta"]

            from src.entities.Cuenta import Cuenta

            cuenta = self.db.query(Cuenta).filter(Cuenta.id_cuenta == id_cuenta).first()

            if not cuenta:
                raise ValueError("La cuenta especificada no existe")

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)

        self.db.commit()
        self.db.refresh(usuario)

        return usuario

    def eliminar_usuario(self, id_usuario: UUID) -> bool:
        """Elimina un usuario."""

        usuario = self.obtener_usuario(id_usuario)

        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True

        return False
