"""
Endpoint de Usuario_App - Endpoints para gestión de usuarios de la app
"""

from typing import List
from uuid import UUID

from crud.Usuario_App_crud import UsuarioAppCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.Usuario_App_schema import (
    UsuarioAppCreate,
    UsuarioAppResponse,
    UsuarioAppUpdate,
)
from schemas.schemas import RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios_app", tags=["usuarios_app"])


@router.get("/", response_model=List[UsuarioAppResponse])
async def obtener_usuarios(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los usuarios de la app.

    Args:
        skip (int, opcional): Número de registros a omitir. Default 0.
        limit (int, opcional): Número máximo de registros a retornar. Default 100.
        db (Session): Sesión de base de datos.

    Returns:
        List[UsuarioAppResponse]: Lista de usuarios registrados.
    """
    try:
        usuario_crud = UsuarioAppCRUD(db)
        usuarios = usuario_crud.obtener_usuariosApp(skip=skip, limit=limit)
        return usuarios

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}",
        )


@router.get("/username/{username}", response_model=UsuarioAppResponse)
async def obtener_usuario_por_username(username: str, db: Session = Depends(get_db)):
    """
    Buscar usuario por username.

    Args:
        username (str): Nombre de usuario.
        db (Session): Sesión de base de datos.

    Returns:
        UsuarioAppResponse: Usuario encontrado.
    """
    try:
        usuario_crud = UsuarioAppCRUD(db)
        usuario = usuario_crud.obtener_usuario_por_username(username)

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        return usuario

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar usuario: {str(e)}",
        )


@router.get("/estado/{estado}", response_model=List[UsuarioAppResponse])
async def obtener_usuarios_por_estado(estado: str, db: Session = Depends(get_db)):
    """
    Buscar usuarios por estado.

    Args:
        estado (str): Estado del usuario (activo, inactivo, bloqueado).
        db (Session): Sesión de base de datos.

    Returns:
        List[UsuarioAppResponse]: Lista de usuarios filtrados por estado.
    """
    try:
        usuario_crud = UsuarioAppCRUD(db)
        usuarios = usuario_crud.obtener_usuarios_por_estado(estado)
        return usuarios

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar usuarios por estado: {str(e)}",
        )


@router.get("/{id_usuario}", response_model=UsuarioAppResponse)
async def obtener_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    """
    Obtener un usuario específico por su ID.

    Args:
        id_usuario (UUID): ID del usuario.
        db (Session): Sesión de base de datos.

    Returns:
        UsuarioAppResponse: Datos del usuario encontrado.
    """
    try:
        usuario_crud = UsuarioAppCRUD(db)
        usuario = usuario_crud.obtener_usuario(id_usuario)

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        return usuario

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.post(
    "/", response_model=UsuarioAppResponse, status_code=status.HTTP_201_CREATED
)
async def crear_usuario(usuario_data: UsuarioAppCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo usuario de la aplicación.

    Args:
        usuario_data (UsuarioAppCreate): Datos del usuario a registrar.
        db (Session): Sesión de base de datos.

    Returns:
        UsuarioAppResponse: Usuario creado exitosamente.
    """
    try:
        usuario_crud = UsuarioAppCRUD(db)

        usuario = usuario_crud.crear_usuario(
            username=usuario_data.username,
            contraseña_hash=usuario_data.contraseña,
            estado=usuario_data.estado,
            id_cuenta=usuario_data.id_cuenta,
        )

        return usuario

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}",
        )


@router.put("/{id_usuario}", response_model=UsuarioAppResponse)
async def actualizar_usuario(
    id_usuario: UUID,
    usuario_data: UsuarioAppUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualizar la información de un usuario existente.

    Args:
        id_usuario (UUID): ID del usuario.
        usuario_data (UsuarioAppUpdate): Campos a actualizar.
        db (Session): Sesión de base de datos.

    Returns:
        UsuarioAppResponse: Usuario actualizado.
    """
    try:
        usuario_crud = UsuarioAppCRUD(db)

        usuario_existente = usuario_crud.obtener_usuario(id_usuario)

        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in usuario_data.dict().items() if v is not None
        }

        usuario_actualizado = usuario_crud.actualizar_usuario(
            id_usuario, **campos_actualizacion
        )

        return usuario_actualizado

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}",
        )


@router.delete("/{id_usuario}", response_model=RespuestaAPI)
async def eliminar_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    """
    Eliminar un usuario de la aplicación.

    Args:
        id_usuario (UUID): ID del usuario.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de éxito si la eliminación fue correcta.
    """
    try:
        usuario_crud = UsuarioAppCRUD(db)

        usuario_existente = usuario_crud.obtener_usuario(id_usuario)

        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        eliminado = usuario_crud.eliminar_usuario(id_usuario)

        if eliminado:
            return RespuestaAPI(
                mensaje="Usuario eliminado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar usuario",
            )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}",
        )
