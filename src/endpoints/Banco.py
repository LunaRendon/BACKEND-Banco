"""
Endpoint de Banco
"""

from typing import List
from uuid import UUID

from src.crud.Banco_crud import BancoCRUD
from src.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.Banco_schema import BancoCreate, BancoResponse, BancoUpdate
from src.schemas.schemas import RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/bancos", tags=["bancos"])


@router.get("", response_model=List[BancoResponse])
async def obtener_bancos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los bancos.

    Args:
        skip (int, opcional): Número de registros a omitir. Default 0.
        limit (int, opcional): Número máximo de registros a retornar. Default 100.
        db (Session): Sesión de base de datos.

    Returns:
        List[BancoResponse]: Lista de todos los bancos registrados.
    """
    try:
        banco_crud = BancoCRUD(db)
        bancos = banco_crud.obtener_bancos(skip=skip, limit=limit)
        return bancos

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener bancos: {str(e)}",
        )


@router.get("/{id_banco}", response_model=BancoResponse)
async def obtener_banco(id_banco: UUID, db: Session = Depends(get_db)):
    """
    Obtener un banco específico por su ID.

    Args:
        id_banco (UUID): ID del banco.
        db (Session): Sesión de base de datos.

    Returns:
        BancoResponse: Datos del banco encontrado.
    """
    try:
        banco_crud = BancoCRUD(db)
        banco = banco_crud.obtener_banco(id_banco)
        if not banco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Banco no encontrado"
            )
        return banco

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener banco: {str(e)}",
        )


@router.post("", response_model=BancoResponse)
async def crear_banco(banco_data: BancoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo banco.

    Args:
        banco_data (BancoCreate): Datos del banco a crear.
        db (Session): Sesión de base de datos.

    Returns:
        BancoResponse: Datos del banco creado.
    """
    try:
        banco_crud = BancoCRUD(db)
        nuevo_banco = banco_crud.crear_banco(
            nombre=banco_data.nombre,
            nit=banco_data.nit,
            direccion=banco_data.direccion,
            telefono=banco_data.telefono,
            correo_contacto=banco_data.correo_contacto,
        )
        return nuevo_banco

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear banco: {str(e)}",
        )


@router.put("/{id_banco}", response_model=BancoResponse)
async def actualizar_banco(
    id_banco: UUID, banco_update: BancoUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar un banco existente.

    Args:
        id_banco (UUID): ID del banco a actualizar.
        banco_update (BancoUpdate): Datos del banco a actualizar.
        db (Session): Sesión de base de datos.

    Returns:
        BancoResponse: Datos del banco actualizado.
    """
    try:
        banco_crud = BancoCRUD(db)
        banco_actualizado = banco_crud.actualizar_banco(
            id_banco,
            nombre=banco_update.nombre,
            nit=banco_update.nit,
            direccion=banco_update.direccion,
            telefono=banco_update.telefono,
            correo_contacto=banco_update.correo_contacto,
        )

        if not banco_actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Banco no encontrado"
            )
        return banco_actualizado

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
            detail=f"Error al actualizar banco: {str(e)}",
        )


@router.delete("/{id_banco}", response_model=RespuestaAPI)
async def eliminar_banco(id_banco: UUID, db: Session = Depends(get_db)):
    """
    Eliminar un banco.

    Args:
        id_banco (UUID): ID del banco a eliminar.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de confirmación de eliminación.
    """
    try:
        banco_crud = BancoCRUD(db)
        eliminado = banco_crud.eliminar_banco(id_banco)

        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Banco no encontrado"
            )

        return RespuestaAPI(mensaje="Banco eliminado exitosamente", exito=True)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar banco: {str(e)}",
        )
