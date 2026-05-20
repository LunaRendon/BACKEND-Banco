"""Pruebas HTTP contra rutas públicas y flujo login + recurso protegido."""

import uuid

from src.database.config import SessionLocal
from src.entities.Usuario_App import Usuario_App
from src.utils.security import hash_password


def test_openapi_documentation_available(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    body = response.json()
    assert "openapi" in body
    assert "paths" in body


def test_login_y_listar_con_token(client):
    """Inserta un usuario directo en BD, hace login y lista usuarios con el token."""
    suffix = uuid.uuid4().hex[:12]
    username = f"pytest_user_{suffix}"
    password = "TestPass12!"

    # 1. Insertar usuario directamente en la BD (saltando el endpoint
    # porque requiere crear Cliente + Cuenta, que escapa al alcance del test)
    db = SessionLocal()
    id_usuario_creado = None
    try:
        usuario = Usuario_App(
            username=username,
            contraseña_hash=hash_password(password),
            estado=True,
            rol="cliente",
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        id_usuario_creado = usuario.id_usuario
    finally:
        db.close()

    try:
        # 2. Login con las credenciales recién creadas
        login_resp = client.post(
            "/usuarios_app/login",
            json={"username": username, "contraseña": password},
        )
        assert login_resp.status_code == 200, f"Login falló: {login_resp.json()}"
        login_body = login_resp.json()
        assert "access_token" in login_body
        assert login_body["token_type"] == "bearer"
        token = login_body["access_token"]
        assert token

        # 3. Listar usuarios con el Bearer token
        lista = client.get(
            "/usuarios_app/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert lista.status_code == 200
        lista_body = lista.json()
        assert isinstance(lista_body, list)

    finally:
        # 4. Limpieza: borrar el usuario creado
        if id_usuario_creado:
            db = SessionLocal()
            try:
                u = db.query(Usuario_App).filter(
                    Usuario_App.id_usuario == id_usuario_creado
                ).first()
                if u:
                    db.delete(u)
                    db.commit()
            finally:
                db.close()