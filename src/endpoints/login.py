"""
Endpoint de Login para Usuario_App.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.core.auth import create_access_token
from src.core.config import get_settings
from src.crud.Usuario_App_crud import UsuarioAppCRUD
from src.database.config import get_db
from src.utils.security import verify_password

router = APIRouter(prefix="/usuarios_app", tags=["auth"])


class LoginData(BaseModel):
    username: str
    contraseña: str


@router.post("/login")
def login(dato: LoginData, db: Session = Depends(get_db)):
    """Autentica un Usuario_App y devuelve un JWT."""
    crud = UsuarioAppCRUD(db)

    usuario = crud.obtener_usuario_por_username(dato.username)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not usuario.estado:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    if not verify_password(dato.contraseña, usuario.contraseña_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    settings = get_settings()
    access_token = create_access_token(
        subject=usuario.id_usuario,
        username=usuario.username,
        rol=usuario.rol,
        settings=settings,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "rol": usuario.rol,
    }
