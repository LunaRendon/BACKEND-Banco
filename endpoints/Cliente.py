"""
Endpoint de Cliente - Endpoints para gestión de cliente
"""

from typing import List
from uuid import UUID

from crud.Cliente_crud import ClienteCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ClienteCreate, ClienteResponse, ClienteUpdate
from schemas.schemas import RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/{id_banco}", response_model=List[ClienteResponse])
async def obtener_clientes(
    id_banco: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los clientes de un banco.

    Args:
        id_banco (UUID): ID del banco.
        skip (int, opcional): Número de registros a omitir. Default 0.
        limit (int, opcional): Número máximo de registros a retornar. Default 100.
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes registrados en el banco.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes(id_banco, skip=skip, limit=limit)
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes: {str(e)}",
        )


@router.get("/{id_banco}/cliente/{id_cliente}", response_model=ClienteResponse)
async def obtener_cliente(
    id_cliente: UUID, id_banco: UUID, db: Session = Depends(get_db)
):
    """
    Obtener un cliente específico por su código.

    Args:
        id_cliente (UUID): ID del cliente.
        id_banco (UUID): ID del banco.
        db (Session): Sesión de base de datos.

    Returns:
        ClienteResponse: Datos del cliente encontrado.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.obtener_cliente(id_cliente, id_banco)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )
        return cliente

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.get("/{id_banco}/nombre/{nombre}", response_model=List[ClienteResponse])
async def obtener_clientes_por_nombre(
    nombre: str, id_banco: UUID, db: Session = Depends(get_db)
):
    """
    Buscar clientes por nombre dentro del banco.

    Args:
        nombre (str): Nombre del cliente o parte del nombre.
        id_banco (UUID): ID del banco.
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes coincidentes.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes_por_nombre(nombre, id_banco)
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por nombre: {str(e)}",
        )


@router.get(
    "/{id_banco}/Documento/{num_documento}", response_model=List[ClienteResponse]
)
async def obtener_clientes_por_NumDocumento(
    num_documento: int, id_banco: UUID, db: Session = Depends(get_db)
):
    """
    Buscar clientes por el numero del documento

    Args:
        num_documento (str): numero del documento del cliente
        id_banco (UUID): ID del banco.
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes con el numero especificado
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes_por_numeroDocumento(
            num_documento, id_banco
        )
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por el numero del documento: {str(e)}",
        )


@router.get("/{id_banco}/tipo/{tipo_documento}", response_model=List[ClienteResponse])
async def obtener_clientes_por_TipoDocumento(
    tipo_documento: str, id_banco: UUID, db: Session = Depends(get_db)
):
    """
    Buscar clientes según el detalle del tipo de cliente.

    Args:
        tipo_documento (str): tipo de documento(CC,TI)
        id_banco (UUID): ID del banco
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes que cumplen con el detalle.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes_por_tipoDocumento(
            tipo_documento, id_banco
        )
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por el tipo del documento: {str(e)}",
        )


@router.get("/{id_banco}/telefono/{telefono}", response_model=List[ClienteResponse])
async def obtener_clientes_por_telefono(
    telefono: int, id_banco: UUID, db: Session = Depends(get_db)
):
    """
    Buscar clientes por telefono

    Args:
        telefono (int): telefono del cliente
        id_banco (UUID): ID del banco
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes filtrados por su telefono
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes_por_telefono(telefono, id_banco)
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por el telefono: {str(e)}",
        )


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo cliente en el banco.

    Args:
        cliente_data (ClienteCreate): Datos del cliente a registrar.
        db (Session): Sesión de base de datos.

    Returns:
        ClienteResponse: Cliente creado exitosamente.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.crear_cliente(
            nombre=cliente_data.nombre,
            num_documento=cliente_data.num_documento,
            tipo_documento=cliente_data.tipo_documento,
            correo=cliente_data.correo,
            telefono=cliente_data.telefono,
            direccion=cliente_data.direccion,
            id_banco=cliente_data.id_banco,
        )
        return cliente

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}",
        )


@router.put("/{id_banco}/cliente/{id_cliente}", response_model=ClienteResponse)
async def actualizar_cliente(
    id_cliente: UUID,
    id_banco: UUID,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualizar la información de un cliente existente.

    Args:
        id_cliente (UUID): ID del cliente.
        id_banco (UUID): ID del banco
        cliente_data (ClienteUpdate): Campos a actualizar.
        db (Session): Sesión de base de datos.

    Returns:
        ClienteResponse: Cliente actualizado.
    """
    try:
        cliente_crud = ClienteCRUD(db)

        cliente_existente = cliente_crud.obtener_cliente(id_cliente, id_banco)
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        campos_actualizacion = {
            k: v
            for k, v in cliente_data.dict().items()
            if v is not None and k != "id_banco"
        }

        cliente_actualizado = cliente_crud.actualizar_cliente(
            id_cliente, id_banco, **campos_actualizacion
        )
        return cliente_actualizado

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}",
        )


@router.delete("/{id_banco}/cliente/{id_cliente}", response_model=RespuestaAPI)
async def eliminar_cliente(
    id_cliente: UUID, id_banco: UUID, db: Session = Depends(get_db)
):
    """
    Eliminar un cliente del banco

    Args:
        id_cliente (UUID): ID del cliente.
        id_banco (UUID): ID del banco
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de éxito si la eliminación fue correcta.
    """
    try:
        cliente_crud = ClienteCRUD(db)

        cliente_existente = cliente_crud.obtener_cliente(id_cliente, id_banco)
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        eliminado = cliente_crud.eliminar_cliente(id_cliente, id_banco)
        if eliminado:
            return RespuestaAPI(mensaje="Cliente eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cliente",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}",
        )
