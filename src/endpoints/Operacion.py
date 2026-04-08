"""
Endpoint de Operacion
"""

from typing import List
from uuid import UUID

from src.crud.Operacion_crud import OperacionCRUD
from src.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.Operacion_schema import (
    OperacionCreate,
    OperacionResponse,
    OperacionUpdate,
)
from src.schemas.schemas import RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/operaciones", tags=["operaciones"])


@router.get("", response_model=List[OperacionResponse])
async def obtener_operaciones(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todas las operaciones.

    Args:
        skip (int, opcional): Número de registros a omitir. Default 0.
        limit (int, opcional): Número máximo de registros a retornar. Default 100.
        db (Session): Sesión de base de datos.

    Returns:
        List[OperacionResponse]: Lista de todas las operaciones registradas.
    """
    try:
        operacion_crud = OperacionCRUD(db)
        operaciones = operacion_crud.obtener_operaciones(skip=skip, limit=limit)
        return operaciones

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener operaciones: {str(e)}",
        )


@router.get("/{id_operacion}", response_model=OperacionResponse)
async def obtener_operacion(id_operacion: UUID, db: Session = Depends(get_db)):
    """
    Obtener una operación específica por su ID.

    Args:
        id_operacion (UUID): ID de la operación.
        db (Session): Sesión de base de datos.

    Returns:
        OperacionResponse: Datos de la operación encontrada.
    """
    try:
        operacion_crud = OperacionCRUD(db)
        operacion = operacion_crud.obtener_operacion(id_operacion)
        if not operacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Operación no encontrada"
            )
        return operacion

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener operación: {str(e)}",
        )


@router.post("", response_model=OperacionResponse, status_code=status.HTTP_201_CREATED)
async def crear_operacion(
    operacion_data: OperacionCreate, db: Session = Depends(get_db)
):
    """
    Crear una nueva operación (depósito, retiro o transferencia).

    Args:
        operacion_data (OperacionCreate): Datos de la operación a crear.
            - tipo_operacion: "deposito", "retiro" o "transferencia"
            - monto: Monto de la operación (debe ser > 0)
            - id_cuenta_origen: ID de la cuenta origen (requerido para retiro y transferencia)
            - id_cuenta_destino: ID de la cuenta destino (requerido para depósito y transferencia)
        db (Session): Sesión de base de datos.

    Returns:
        OperacionResponse: Datos de la operación creada.
    """
    try:
        operacion_crud = OperacionCRUD(db)
        nueva_operacion = operacion_crud.crear_operacion(
            tipo_operacion=operacion_data.tipo_operacion,
            monto=operacion_data.monto,
            id_cuenta_origen=operacion_data.id_cuenta_origen,
            id_cuenta_destino=operacion_data.id_cuenta_destino,
        )
        return nueva_operacion

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear operación: {str(e)}",
        )


@router.put("/{id_operacion}", response_model=OperacionResponse)
async def actualizar_operacion(
    id_operacion: UUID, operacion_update: OperacionUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar una operación existente.

    Args:
        id_operacion (UUID): ID de la operación a actualizar.
        operacion_update (OperacionUpdate): Datos de la operación a actualizar.
        db (Session): Sesión de base de datos.

    Returns:
        OperacionResponse: Datos de la operación actualizada.
    """
    try:
        operacion_crud = OperacionCRUD(db)
        operacion_actualizada = operacion_crud.actualizar_operacion(
            id_operacion,
            tipo_operacion=operacion_update.tipo_operacion,
            monto=operacion_update.monto,
            id_cuenta_origen=operacion_update.id_cuenta_origen,
            id_cuenta_destino=operacion_update.id_cuenta_destino,
        )

        if not operacion_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Operación no encontrada",
            )
        return operacion_actualizada

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar operación: {str(e)}",
        )


@router.delete("/{id_operacion}", response_model=RespuestaAPI)
async def eliminar_operacion(id_operacion: UUID, db: Session = Depends(get_db)):
    """
    Eliminar una operación.

    Args:
        id_operacion (UUID): ID de la operación a eliminar.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de confirmación de eliminación.
    """
    try:
        operacion_crud = OperacionCRUD(db)
        eliminada = operacion_crud.eliminar_operacion(id_operacion)

        if not eliminada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Operación no encontrada",
            )

        return RespuestaAPI(
            mensaje="Operación eliminada exitosamente",
            exito=True,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar operación: {str(e)}",
        )
