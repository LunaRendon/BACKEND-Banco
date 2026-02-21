class Cliente:
    """
    Representa un cliente del banco.
    """

    def _init_(
        self,
        id_cliente: int,
        nombre: str,
        num_documento: int,
        tipo_documento: str,
        correo: str,
        telefono: int,
        direccion: str,
    ):
        """
        Inicializa un nuevo cliente.

        Args:
            id_cliente (int): Código único del cliente.
            nombre (str): Nombre completo del cliente.
            num_documento (int): numero del documento del cliente
            tipo_documento (str): Detalle adicional del documento(CC,TI)
            correo (str) : correo electronico del cliente
            telefono (int): telefono del cliente
            direccion (str): direccion de residencia del cliente
        """
        self.id_cliente = (id_cliente,)
        self.nombre = (nombre,)
        self.num_documento = (num_documento,)
        self.tipo_documento = (tipo_documento,)
        self.correo = (correo,)
        self.telefono = (telefono,)
        self.direccion = direccion

    def _str_(self) -> str:
        """
        Representación en cadena del cliente.

        Returns:
            str: Información completa del cliente en formato legible.
        """
        return f"Código: {self.num_documento}, Nombre: {self.nombre}, Correo: {self.correo}, Telefono: {self.telefono}, Direccion:{self.direccion}"
