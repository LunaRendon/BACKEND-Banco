"""
Endpoint de Tarjeta - Endpoints para gestión de tarjetas
"""

from typing import List
from uuid import UUID

from src.crud.Tarjeta_crud import TarjetaCRUD
from src.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.Tarjeta_schema import TarjetaCreate, TarjetaResponse, TarjetaUpdate
from src.schemas.schemas import RespuestaAPI
from src.core.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/tarjetas",
    tags=["tarjetas"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=List[TarjetaResponse])
async def obtener_todas_tarjetas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todas las tarjetas registradas.
    Args:
        skip (int): Número de registros a omitir para paginación.
        limit (int): Número máximo de registros a retornar para paginación.
        db (Session): Sesión de base de datos.
    Returns:
        List[TarjetaResponse]: Lista de todas las tarjetas registradas.
    """
    try:
        tarjeta_crud = TarjetaCRUD(db)
        tarjetas = tarjeta_crud.obtener_tarjetas(skip=skip, limit=limit)
        return tarjetas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tarjetas: {str(e)}",
        )


@router.get("/{id_cuenta}", response_model=List[TarjetaResponse])
async def obtener_tarjetas(
    id_cuenta: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todas las tarjetas asociadas a una cuenta.

    Args:
        id_cuenta (UUID): ID de la cuenta para filtrar las tarjetas.
        skip (int): Número de registros a omitir para paginación.
        limit (int): Número máximo de registros a retornar para paginación.
        db (Session): Sesión de base de datos.
    Returns:
        List[TarjetaResponse]: Lista de tarjetas asociadas a la cuenta.
    """
    try:
        tarjeta_crud = TarjetaCRUD(db)
        tarjetas = tarjeta_crud.obtener_tarjetas(id_cuenta, skip=skip, limit=limit)
        return tarjetas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tarjetas: {str(e)}",
        )


@router.get("/{id_cuenta}/tarjeta/{id_tarjeta}", response_model=TarjetaResponse)
async def obtener_tarjeta(
    id_tarjeta: UUID, id_cuenta: UUID, db: Session = Depends(get_db)
):
    """
    Obtener una tarjeta específica.

    Args:
        id_tarjeta (UUID): ID de la tarjeta a obtener.
        id_cuenta (UUID): ID de la cuenta a la que pertenece la tarjeta.
        db (Session): Sesión de base de datos.
    Returns:
        TarjetaResponse: Detalles de la tarjeta solicitada.
    """
    try:
        tarjeta_crud = TarjetaCRUD(db)
        tarjeta = tarjeta_crud.obtener_tarjeta(id_tarjeta, id_cuenta)

        if not tarjeta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarjeta no encontrada",
            )

        return tarjeta

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tarjeta: {str(e)}",
        )


@router.get(
    "/{id_cuenta}/numero/{numero_tarjeta}", response_model=List[TarjetaResponse]
)
async def obtener_tarjetas_por_numero(
    numero_tarjeta: str, id_cuenta: UUID, db: Session = Depends(get_db)
):
    """
    Buscar tarjetas por número.

    Args:
        numero_tarjeta (str): Número de la tarjeta a buscar.
        id_cuenta (UUID): ID de la cuenta a la que pertenecen las tarjetas.

    Returns:
        List[TarjetaResponse]: Lista de tarjetas que coinciden con el número y la cuenta.
    """
    try:
        tarjeta_crud = TarjetaCRUD(db)
        tarjetas = tarjeta_crud.obtener_tarjetas_por_numero(numero_tarjeta, id_cuenta)
        return tarjetas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar tarjetas por número: {str(e)}",
        )


@router.get("/{id_cuenta}/tipo/{tipo_tarjeta}", response_model=List[TarjetaResponse])
async def obtener_tarjetas_por_tipo(
    tipo_tarjeta: str, id_cuenta: UUID, db: Session = Depends(get_db)
):
    """
    Buscar tarjetas por tipo.

    args:
        tipo_tarjeta (str): Tipo de tarjeta (e.g., "débito", "crédito").
        id_cuenta (UUID): ID de la cuenta a la que pertenecen las tarjetas.

        Returns: List[TarjetaResponse]: Lista de tarjetas que coinciden con el tipo y la cuenta.
    """
    try:
        tarjeta_crud = TarjetaCRUD(db)
        tarjetas = tarjeta_crud.obtener_tarjetas_por_tipo(tipo_tarjeta, id_cuenta)
        return tarjetas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar tarjetas por tipo: {str(e)}",
        )


@router.get("/{id_cuenta}/estado/{estado}", response_model=List[TarjetaResponse])
async def obtener_tarjetas_por_estado(
    estado: bool, id_cuenta: UUID, db: Session = Depends(get_db)
):
    """
    Buscar tarjetas por estado.

    args:
        estado (bool): Estado de la tarjeta.
        id_cuenta (UUID): ID de la cuenta a la que pertenecen las tarjetas.

        Returns: List[TarjetaResponse]: Lista de tarjetas que coinciden con el estado y la cuenta.
    """
    try:
        tarjeta_crud = TarjetaCRUD(db)
        tarjetas = tarjeta_crud.obtener_tarjetas_por_estado(estado, id_cuenta)
        return tarjetas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar tarjetas por estado: {str(e)}",
        )


@router.post("/", response_model=TarjetaResponse, status_code=status.HTTP_201_CREATED)
async def crear_tarjeta(tarjeta_data: TarjetaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva tarjeta.

    Args:
        tarjeta_data (TarjetaCreate): Datos de la tarjeta a crear.
        db (Session): Sesión de base de datos.

    Returns:
        TarjetaResponse: Tarjeta creada exitosamente.
    """
    try:
        tarjeta_crud = TarjetaCRUD(db)

        tarjeta = tarjeta_crud.crear_tarjeta(
            numero_tarjeta=tarjeta_data.numero_tarjeta,
            tipo_tarjeta=tarjeta_data.tipo_tarjeta,
            fecha_vencimiento=tarjeta_data.fecha_vencimiento,
            cvv=tarjeta_data.cvv,
            estado=tarjeta_data.estado,
            id_cuenta=tarjeta_data.id_cuenta,
        )

        return tarjeta

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear tarjeta: {str(e)}",
        )


@router.put("/{id_cuenta}/tarjeta/{id_tarjeta}", response_model=TarjetaResponse)
async def actualizar_tarjeta(
    id_tarjeta: UUID,
    id_cuenta: UUID,
    tarjeta_data: TarjetaUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualizar una tarjeta existente.

    Args:
        id_tarjeta (UUID): ID de la tarjeta.
        id_cuenta (UUID): ID de la cuenta.
        tarjeta_data (TarjetaUpdate): Campos a actualizar.
        db (Session): Sesión de base de datos.

    Returns:
        TarjetaResponse: Tarjeta actualizada.
    """
    try:
        tarjeta_crud = TarjetaCRUD(db)

        tarjeta_existente = tarjeta_crud.obtener_tarjeta(id_tarjeta, id_cuenta)

        if not tarjeta_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarjeta no encontrada",
            )

        campos_actualizacion = {
            k: v
            for k, v in tarjeta_data.dict().items()
            if v is not None and k != "id_cuenta"
        }

        tarjeta_actualizada = tarjeta_crud.actualizar_tarjeta(
            id_tarjeta, id_cuenta, **campos_actualizacion
        )

        return tarjeta_actualizada

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar tarjeta: {str(e)}",
        )


@router.delete("/{id_cuenta}/tarjeta/{id_tarjeta}", response_model=RespuestaAPI)
async def eliminar_tarjeta(
    id_tarjeta: UUID, id_cuenta: UUID, db: Session = Depends(get_db)
):
    """
    Eliminar una tarjeta de una cuenta.
    Args:
        id_tarjeta (UUID): ID de la tarjeta.
        id_cuenta (UUID): ID de la cuenta.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de éxito si la eliminación fue correcta.
    """
    try:
        tarjeta_crud = TarjetaCRUD(db)

        tarjeta_existente = tarjeta_crud.obtener_tarjeta(id_tarjeta, id_cuenta)

        if not tarjeta_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarjeta no encontrada",
            )

        eliminado = tarjeta_crud.eliminar_tarjeta(id_tarjeta, id_cuenta)

        if eliminado:
            return RespuestaAPI(
                mensaje="Tarjeta eliminada exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar tarjeta",
            )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar tarjeta: {str(e)}",
        )
