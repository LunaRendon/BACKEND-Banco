"""
Seeder: datos iniciales para Banco y Usuario (admin).
Idempotente: no duplica registros si ya existen.

Uso:
  python seed_db.py

Requiere DATABASE_URL. Ejecutar después de migrate_db.py.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from sqlalchemy.exc import OperationalError

from src.database.config import SessionLocal
from src.entities.Banco import Banco
from src.entities.Usuario import Usuario
from src.auth.security import PasswordManager


"""
Datos iniciales para las entidades Banco y Usuario.
"""

BANCO_INICIAL = {
    "nombre": "Banco Central",
    "nit": "900123456-7",
    "direccion": "Calle 10 # 20-30",
    "telefono": "+57 300 123 4567",
    "correo_contacto": "contacto@banco.com",
}

USUARIO_INICIAL = {
    "nombre": "Admin",
    "nombre_usuario": "admin",
    "email": "admin@banco.local",
    "contraseña": "Admin123!",
    "es_admin": True,
}


"""
Crea el banco si no existe en la base de datos.
"""


def seed_banco(db):
    banco = db.query(Banco).filter(Banco.nit == BANCO_INICIAL["nit"]).first()
    if banco:
        return banco

    banco = Banco(**BANCO_INICIAL)
    db.add(banco)
    db.commit()
    db.refresh(banco)

    print("  Banco creado: Banco Central")
    return banco


"""
Crea el usuario administrador si no existe.
"""


def get_or_create_admin(db):
    admin = (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == USUARIO_INICIAL["nombre_usuario"])
        .first()
    )

    if admin:
        return admin

    u = USUARIO_INICIAL.copy()
    u["contraseña_hash"] = PasswordManager.hash_password(u.pop("contraseña"))

    admin = Usuario(**u)
    db.add(admin)
    db.commit()
    db.refresh(admin)

    print("  Usuario creado: admin")
    return admin


"""
Función principal que ejecuta el proceso de seed.
"""


def main():
    try:
        db = SessionLocal()
        try:
            print("Sembrando banco...")
            seed_banco(db)

            print("Sembrando usuario admin...")
            get_or_create_admin(db)

            print("Seed completado.")
        finally:
            db.close()

    except OperationalError as e:
        print("Error de conexión a la base de datos:", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
