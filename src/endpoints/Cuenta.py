"""
Endpoint de Cuenta - Endpoints para gestión de cuentas
"""

from typing import List
from uuid import UUID

from src.crud.Cuenta_crud import CuentaCRUD
from src.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import CuentaCreate, CuentaResponse, CuentaUpdate
from schemas.schemas import RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cuentas", tags=["cuentas"])


@router.get("/{id_cliente}", response_model=List[CuentaResponse])
async def obtener_cuentas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todas las cuentas.

    Args:
        skip (int, opcional): Número de registros a omitir. Default 0.
        limit (int, opcional): Número máximo de registros a retornar. Default 100.
        db (Session): Sesión de base de datos.

    Returns:
        List[CuentaResponse]: Lista de cuentas registradas a ese cliente.
    """
    try:
        cuenta_crud = CuentaCRUD(db)
        cuentas = cuenta_crud.obtener_cuentas(skip=skip, limit=limit)
        return cuentas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las cuentas: {str(e)}",
        )


@router.get("/{id_cliente}/cuenta/{id_cuenta}", response_model=CuentaResponse)
async def obtener_cuenta(
    id_cliente: UUID, id_cuenta: UUID, db: Session = Depends(get_db)
):
    """
    Obtener una cuenta en específico por su código.

    Args:
        id_cliente (UUID): ID del cliente.
        id_cuenta (UUID): ID de la cuenta.
        db (Session): Sesión de base de datos.

    Returns:
        CuentaResponse: Datos de la cuenta encontrada.
    """
    try:
        cuenta_crud = CuentaCRUD(db)
        cuenta = cuenta_crud.obtener_cuenta(id_cuenta, id_cliente)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )
        return cuenta

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la cuenta: {str(e)}",
        )


@router.get(
    "/{id_cliente}/tipo de cuenta/{tipo_cuenta}", response_model=List[CuentaResponse]
)
async def obtener_cuentas_por_tipodCuenta(
    tipo_cuenta: str, id_cliente: UUID, db: Session = Depends(get_db)
):
    """
    Buscar clientes por nombre dentro del banco.

    Args:
        tipo_cuenta (str): tipo de la cuenta (Ahorros/Corriente)
        id_cliente (UUID): ID del cliente.
        db (Session): Sesión de base de datos.

    Returns:
        List[CuentaResponse]: Lista de cuentas coincidentes.
    """
    try:
        cuenta_crud = CuentaCRUD(db)
        cuentas = cuenta_crud.obtener_cuentas_por_tipodCuentas(tipo_cuenta, id_cliente)
        return cuentas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por nombre: {str(e)}",
        )


@router.get("/{id_cliente}/Estado/{estado}", response_model=List[CuentaResponse])
async def obtener_cuentas_por_estado(
    estado: str, id_cliente: UUID, db: Session = Depends(get_db)
):
    """
    Buscar cuentas por el estado actual

    Args:
        id_cliente (str): id del cliente
        esatdo (UUID): estado actual de la cuenta
        db (Session): Sesión de base de datos.

    Returns:
        List[CuentaResponse]: Lista de cuentas con el estado especificado
    """
    try:
        cuenta_crud = CuentaCRUD(db)
        cuentas = cuenta_crud.obtener_cuentas_por_estado(estado, id_cliente)
        return cuentas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar cuentas por el estado: {str(e)}",
        )


@router.get(
    "/{id_cliente}/Numero documento/{numero_cuenta}",
    response_model=List[CuentaResponse],
)
async def obtener_cuentas_por_numerodCuenta(
    numero_cuenta: int, id_cliente: UUID, db: Session = Depends(get_db)
):
    """
    Buscar cuentas según el numero de la cuenta

    Args:
        numero_cuenta (int): numero de la cuenta
        id_cliente (UUID): id del cliente
        db (Session): Sesión de base de datos.

    Returns:
        List[CuentaResponse]: Lista de cuentas que cumplen con el numero especificado
    """
    try:
        cuenta_crud = CuentaCRUD(db)
        cuentas = cuenta_crud.obtener_cuenta_por_numeroCuenta(numero_cuenta, id_cliente)
        return cuentas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar cuentas por el numero especificado: {str(e)}",
        )


@router.post("/", response_model=CuentaResponse, status_code=status.HTTP_201_CREATED)
async def crear_cuenta(cuenta_data: CuentaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva cuenta en el banco.

    Args:
        cuenta_data (CuentaCreate): Datos de la cuenta a registrar.
        db (Session): Sesión de base de datos.

    Returns:
        CuentaResponse: Cuenta creada exitosamente.
    """
    try:
        cuenta_crud = CuentaCRUD(db)
        cuenta = cuenta_crud.crear_cuenta(
            numero_cuenta=cuenta_data.numero_cuenta,
            tipo_cuenta=cuenta_data.tipo_cuenta,
            saldo=cuenta_data.saldo,
            fecha_apertura=cuenta_data.fecha_apertura,
            estado=cuenta_data.estado,
            id_cliente=cuenta_data.id_cliente,
        )
        return cuenta

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la cuenta: {str(e)}",
        )


@router.put("/{id_cliente}/Cuenta/{id_cuenta}", response_model=CuentaResponse)
async def actualizar_cuenta(
    id_cliente: UUID,
    id_cuenta: UUID,
    cuenta_data: CuentaUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualizar la información de una cuenta existente.

    Args:
        id_cliente (UUID): ID del cliente.
        id_cuenta (UUID): ID de la cuenta
        cuenta_data (ClienteUpdate): Campos a actualizar.
        db (Session): Sesión de base de datos.

    Returns:
        CuentaResponse: Cuenta actualizado.
    """
    try:
        cuenta_crud = CuentaCRUD(db)
        cuenta_existente = cuenta_crud.obtener_cuenta(id_cuenta, id_cliente)
        if not cuenta_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )
        campos_actualizacion = {
            k: v
            for k, v in cuenta_data.dict().items()
            if v is not None and k != "id_cliente"
        }

        cuenta_actualizada = cuenta_crud.actualizar_cuenta(
            id_cuenta, id_cliente, **campos_actualizacion
        )
        return cuenta_actualizada

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la cuenta: {str(e)}",
        )


@router.delete("/{id_cliente}/Cuenta/{id_cuenta}", response_model=RespuestaAPI)
async def eliminar_cuenta(
    id_cuenta: UUID, id_cliente: UUID, db: Session = Depends(get_db)
):
    """
    Eliminar una cuenta de un cliente del banco

    Args:
        id_cuenta (UUID): id de la cuenta
        id_cliete (UUID): ID del cliente.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de éxito si la eliminación fue correcta.
    """
    try:
        cuenta_crud = CuentaCRUD(db)

        cuenta_existente = cuenta_crud.obtener_cuenta(id_cuenta, id_cliente)
        if not cuenta_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )

        eliminada = cuenta_crud.eliminar_cuenta(id_cuenta, id_cliente)
        if eliminada:
            return RespuestaAPI(mensaje="Cuenta eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la cuenta",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la cuenta: {str(e)}",
        )
