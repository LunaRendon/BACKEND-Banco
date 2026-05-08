"""
Endpoint de Prestamos - Endpoints para gestión de prestamos
"""

from typing import List
from uuid import UUID

from src.crud.Prestamos_crud import PrestamoCRUD
from src.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.Prestamo_schema import PrestamoCreate, PrestamoResponse, PrestamoUpdate
from src.schemas.schemas import RespuestaAPI
from sqlalchemy.orm import Session
from src.core.auth import get_current_user
from fastapi import Depends
import traceback

router = APIRouter(
    prefix="/prestamos",
    tags=["prestamos"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=List[PrestamoResponse])
async def obtener_todos_prestamos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        Prestamo_crud = PrestamoCRUD(db)
        Prestamos = Prestamo_crud.obtener_todos_prestamos(skip=skip, limit=limit)
        return Prestamos

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los préstamos: {str(e)}",
        )


@router.get("/{id_cliente}", response_model=List[PrestamoResponse])
async def obtener_prestamos(
    id_cliente: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        Prestamo_crud = PrestamoCRUD(db)
        prestamos = Prestamo_crud.obtener_prestamos(id_cliente, skip=skip, limit=limit)
        return prestamos

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el prestamo: {str(e)}",
        )


@router.get("/{id_cliente}/prestamo/{id_prestamo}", response_model=PrestamoResponse)
async def obtener_prestamo(
    id_prestamo: UUID, id_cliente: UUID, db: Session = Depends(get_db)
):
    try:
        Prestamo_crud = PrestamoCRUD(db)
        prestamo = Prestamo_crud.obtener_prestamo(id_prestamo, id_cliente)
        if not prestamo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado"
            )
        return prestamo

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el prestamo: {str(e)}",
        )


@router.get("/{id_cliente}/cliente/{id_cuenta}", response_model=List[PrestamoResponse])
async def obtener_prestamos_por_cuenta(
    id_cliente: UUID, id_cuenta: UUID, db: Session = Depends(get_db)
):
    try:
        Prestamos_crud = PrestamoCRUD(db)
        prestamos = Prestamos_crud.obtener_prestamos_por_cliente(id_cliente, id_cuenta)
        if not prestamos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado"
            )
        return prestamos

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el prestamo: {str(e)}",
        )


@router.post("", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
async def crear_prestamo(
    prestamo_data: PrestamoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        Prestamos_crud = PrestamoCRUD(db)
        prestamos = Prestamos_crud.crear_prestamo(
            monto=prestamo_data.monto,
            interes=prestamo_data.interes,
            cuotas=prestamo_data.cuotas,
            estado=prestamo_data.estado,
            fecha_inicio=prestamo_data.fecha_inicio,
            fecha_fin=prestamo_data.fecha_fin,
            id_cliente=prestamo_data.id_cliente,
            id_cuenta=prestamo_data.id_cuenta,
            id_usuario_crea=current_user.id_usuario,
        )
        return prestamos

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el prestamo: {str(e)}",
        )


@router.put("/{id_cliente}/{id_prestamo}", response_model=PrestamoResponse)
async def actualizar_prestamo(
    id_prestamo: UUID,
    id_cliente: UUID,
    prestamo_data: PrestamoUpdate,
    db: Session = Depends(get_db),
):
    try:
        Prestamos_cud = PrestamoCRUD(db)

        prestamos_existentes = Prestamos_cud.obtener_prestamo(id_prestamo, id_cliente)
        if not prestamos_existentes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado"
            )

        campos_actualizacion = {
            k: v
            for k, v in prestamo_data.dict().items()
            if v is not None and k != "id_biblioteca"
        }

        if not campos_actualizacion:
            return prestamos_existentes

        prestamo_actualizado = Prestamos_cud.actualizar_prestamo(
            id_prestamo, id_cliente, **campos_actualizacion
        )
        return prestamo_actualizado

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el prestamo: {str(e)}",
        )


@router.delete("/{id_cliente}/{id_prestamo}", response_model=RespuestaAPI)
async def eliminar_prestamo(
    id_cliente: UUID, id_prestamo: UUID, db: Session = Depends(get_db)
):
    try:
        Prestamos_crud = PrestamoCRUD(db)

        prestamo_existente = Prestamos_crud.obtener_prestamo(id_prestamo, id_cliente)
        if not prestamo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado"
            )

        eliminada = Prestamos_crud.eliminar_prestamo(id_prestamo, id_cliente)
        if eliminada:
            return RespuestaAPI(mensaje="Prestamo eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el prestamo",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el prestamo: {str(e)}",
        )
