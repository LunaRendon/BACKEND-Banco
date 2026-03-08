"""
Menú por consola que usa el CRUD (cliente de la API).
Al ejecutar main.py se inicia la API en segundo plano (uvicorn) y luego el menú.
"""

import sys
import threading
import time
from uuid import UUID

# Permitir importar desde src cuando se ejecuta desde la raíz del proyecto
sys.path.insert(0, ".")

from crud.Usuario_crud import UsuarioCRUD
from crud.Banco_crud import BancoCRUD
from crud.Cliente_crud import ClienteCRUD
from crud.Cuenta_crud import CuentaCRUD
from crud.Operacion_crud import OperacionCRUD
from crud.Tarjeta_crud import TarjetaCRUD
from crud.Usuario_App_crud import UsuarioAppCRUD


def mostrar_usuarios():
    try:
        usuarios = UsuarioCRUD.obtener_usuarios()
        if not usuarios:
            print("  No hay usuarios.")
            return
        for u in usuarios:
            print(
                f"  {u['id']} | {u['nombre_usuario']} | {u['email']} | activo={u['activo']}"
            )
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print(
                "  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar."
            )
        else:
            print(f"  Error: {e}")


def menu_bancos():
    bancos_crud = BancoCRUD
    while True:
        print("\n--- Bancos ---")
        print(
            "1. Listar \n 2. Ver uno \n 3. Crear \n 4. Actualizar \n 5. Eliminar \n 0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            bancos_crud.obtener_bancos
        elif op == "2":
            bid = UUID(input("ID banco: "))
            if bid:
                try:
                    b = bancos_crud.obtener_banco(bid)
                    print(f"  {b}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            nombre = input("Nombre: ").strip()
            nit = input("NIT: ").strip()
            direccion = input("Direccion: ").strip()
            telefono = input("Telefono: ").strip()
            correo_contacto = input("Correo de contacto: ").strip()
            if nombre and nit and direccion and telefono and correo_contacto:
                try:
                    bancos_crud.crear_banco(
                        nombre, nit, direccion, telefono, correo_contacto
                    )
                    print("  Banco creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        elif op == "4":
            uid = input("ID banco: ").strip()
            if not uid:
                continue
            nombre = input("Nombre: ").strip()
            telefono = input("Telefono: ").strip()
            direccion = input("Direccion: ").strip()
            correo_contacto = input("Correo de contacto: ").strip()
            try:
                kwargs = {}
                if nombre:
                    kwargs["nombre"] = nombre
                if telefono:
                    kwargs["telefono"] = telefono
                if direccion:
                    kwargs["direccion"] = direccion
                if correo_contacto:
                    kwargs["correo_contacto"] = correo_contacto
                bancos_crud.actualizar_banco(uid, **kwargs)
                print("  Banco actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            uid = input("ID banco a eliminar: ").strip()
            if uid:
                try:
                    bancos_crud.eliminar_banco(uid)
                    print("  Banco eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")


def menu_clientes():
    while True:
        print("\n--- Clientes ---")
        print(
            "1. Listar \n 2. Ver uno \n 3. Crear \n 4. Actualizar \n 5. Eliminar \n 0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            ClienteCRUD.obtener_clientes()
        elif op == "2":
            cid = input("ID del cliente: ").strip()
            if cid:
                try:
                    c = ClienteCRUD.obtener_cliente(cid)
                    print(f"  {c}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            nombre = input("Nombre del cliente: ").strip()
            num_documento = input("Numero de documento: ").strip()
            tipo_documento = input("Tipo de documento: ").strip() or None
            correo = input("Correo electronico: ").strip() or None
            telefono = input("Telefono: ").strip() or None
            direccion = input("Direccion: ").strip()
            id_banco = input("ID banco al que pertenecera: ").strip()
            id_usuario = input("ID usuario creador: ").strip()
            if (
                nombre
                and num_documento
                and tipo_documento
                and correo
                and telefono
                and direccion
                and id_banco
                and id_usuario
            ):
                try:
                    ClienteCRUD.crear_cliente(
                        nombre,
                        num_documento,
                        tipo_documento,
                        correo,
                        telefono,
                        direccion,
                        id_banco,
                        id_usuario,
                    )
                    print("  Cliente creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan variable o ID usuario.")
        elif op == "4":
            cid = input("ID cliente: ").strip()
            if not cid:
                continue
            nombre = input("Nombre del cliente: ").strip()
            tipo_documento = input("Tipo de documento: ").strip() or None
            correo = input("Correo electronico: ").strip() or None
            telefono = input("Telefono: ").strip() or None
            direccion = input("Direccion: ").strip()
            id_banco = input("ID banco al que pertenecera: ").strip()
            try:
                kwargs = {}
                if nombre:
                    kwargs["nombre"] = nombre
                if tipo_documento:
                    kwargs["tipo_documento"] = tipo_documento
                if correo:
                    kwargs["correo"] = correo
                if telefono:
                    kwargs["telefono"] = telefono
                if direccion:
                    kwargs["direccion"] = direccion
                if id_banco:
                    kwargs["id_banco"] = id_banco
                ClienteCRUD.actualizar_cliente(cid, **kwargs)
                print("  Cliente actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            cid = input("ID cliente a eliminar: ").strip()
            if cid:
                try:
                    ClienteCRUD.eliminar_cliente(cid)
                    print("  Cliente eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")


def menu_cuentas():
    while True:
        print("\n--- Cuentas ---")
        print(
            "1. Listar \n 2. Ver uno \n 3. Crear \n 4. Actualizar \n  5. Eliminar \n  0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            CuentaCRUD.obtener_cuentas()
        elif op == "2":
            cid = input("ID de la cuenta: ").strip()
            if cid:
                try:
                    c = CuentaCRUD.obtener_cuenta(cid)
                    print(f"  {c}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            numero_cuenta = input("Numero de la cuenta ").strip()
            tipo_cuenta = input("Tipo de la cuenta (Ahorros/Corriente): ").strip()
            saldo = input("Saldo inicial de la cuenta: ").strip()
            fecha_apertura = input("Fecha de apertura de la cuenta: ").strip()
            estado = input("Estado de la cuenta: ").strip()
            id_cliente = input("Id del cliente al que pertenecera la cuenta: ").strip()
            id_usuario = input("ID usuario creador: ").strip()
            if (
                numero_cuenta
                and tipo_cuenta
                and saldo
                and fecha_apertura
                and estado
                and id_cliente
                and id_usuario
            ):
                try:
                    CuentaCRUD.crear_cuenta(
                        numero_cuenta,
                        tipo_cuenta,
                        saldo,
                        fecha_apertura,
                        estado,
                        id_cliente,
                        id_usuario,
                    )
                    print("  Cuenta creada.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan variable o ID usuario.")
        elif op == "4":
            cid = input("ID cuenta: ").strip()
            if not cid:
                continue
            tipo_cuenta = input("Nuevo tipo de cuenta: ").strip()
            estado = input("Nuevo estado de cuenta: ").strip()
            try:
                kwargs = {}
                if tipo_cuenta:
                    kwargs["tipo_cuenta"] = tipo_cuenta
                if estado:
                    kwargs["estado"] = estado
                CuentaCRUD.actualizar_cuenta(cid, **kwargs)
                print("  Cuenta actualizada.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            oid = input("ID cuenta a eliminar: ").strip()
            if oid:
                try:
                    CuentaCRUD.eliminar_cuenta(oid)
                    print("  Cuenta eliminada.")
                except Exception as e:
                    print(f"  Error: {e}")


def menu_operaciones():
    while True:
        print("\n--- Operaciones ---")
        print("1. Listar \n 2. Ver uno \n 3. Crear \n 4. Eliminar \n 0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            OperacionCRUD.obtener_operaciones()
        elif op == "2":
            oid = input("ID de la la operación: ").strip()
            if oid:
                try:
                    o = OperacionCRUD.obtener_operacion(oid)
                    print(f"  {o}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            crear_operacion_menu()
        elif op == "4":
            cid = input("ID operacion  a eliminar: ").strip()
            if cid:
                try:
                    OperacionCRUD.eliminar_operacion(cid)
                    print("  Operacion eliminada.")
                except Exception as e:
                    print(f"  Error: {e}")


def crear_operacion_menu():
    print("\n--- Crear operación ---")
    print("1. Depósito \n 2. Retiro \n 3. Transferencia")
    tipo = input("Seleccione tipo: ").strip()
    monto = input("Monto: ").strip()
    id_usuario = input("ID usuario creador: ").strip()
    if tipo == "1":
        id_cuenta_destino = input("ID cuenta destino: ").strip()

        OperacionCRUD.crear_operacion(
            "deposito", monto, None, id_cuenta_destino, id_usuario
        )
    elif tipo == "2":
        id_cuenta_origen = input("ID cuenta origen: ").strip()
        OperacionCRUD.crear_operacion(
            "retiro", monto, id_cuenta_origen, None, id_usuario
        )
    elif tipo == "3":
        id_cuenta_origen = input("ID cuenta origen: ").strip()
        id_cuenta_destino = input("ID cuenta destino: ").strip()

        OperacionCRUD.crear_operacion(
            "transferencia", monto, id_cuenta_origen, id_cuenta_destino, id_usuario
        )
    else:
        print("Tipo de operación no válido.")


def menu_tarjetas():
    while True:
        print("\n--- Tarjetas ---")
        print(
            "1. Listar \n 2. Ver uno \n 3. Crear \n 4. Actualizar \n  5. Actulizar estado \n 6. Eliminar \n  0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            TarjetaCRUD.obtener_tarjetas()
        elif op == "2":
            tid = input("ID de la tarjeta: ").strip()
            if tid:
                try:
                    t = TarjetaCRUD.obtener_tarjeta(tid)
                    print(f"  {t}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            numero_tarjeta = input("Numero de la tarjeta ").strip()
            tipo_tarjeta = input("Tipo de la tarjeta (Credito/Debito): ").strip()
            fecha_vencimiento = input("Fecha en la que vencera: ").strip()
            cvv = input("Codigo de seguridad de la tarjeta: ").strip()
            estado = input("Estado de la tarjeta: ").strip()
            id_cuenta = input("Id de la cuenta a la que pertenece la tarjeta: ").strip()
            id_usuario = input("ID usuario creador: ").strip()
            if (
                numero_tarjeta
                and tipo_tarjeta
                and fecha_vencimiento
                and cvv
                and estado
                and id_cuenta
                and id_usuario
            ):
                try:
                    TarjetaCRUD.crear_tarjeta(
                        numero_tarjeta,
                        tipo_tarjeta,
                        fecha_vencimiento,
                        cvv,
                        estado,
                        id_cuenta,
                        id_usuario,
                    )
                    print("  Tarjeta creada.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan variable o ID usuario.")
        elif op == "4":
            tid = input("ID tarjeta: ").strip()
            if not tid:
                continue
            tipo_tarjeta = input("Nuevo tipo de tarjera: ").strip() or None
            fecha_vencimiento = input("Nueva fecha vencimiento de la tarjeta: ").strip()
            cvv = input("Nuevo cvv de la tarjeta: ").strip()
            try:
                kwargs = {}
                if tipo_tarjeta:
                    kwargs["tipo_tarjeta"] = tipo_tarjeta
                if fecha_vencimiento:
                    kwargs["fecha_vencimiento"] = fecha_vencimiento
                if cvv:
                    kwargs["cvv"] = cvv
                TarjetaCRUD.actualizar_tarjeta(tid, **kwargs)
                print("  Tarjeta actualizada.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            tid = input("ID tarjeta: ").strip()
            if not tid:
                continue
            estado = input("Nuevo estado de la tarjeta: ").strip()
            try:
                kwargs = {}
                if estado:
                    kwargs["estado"] = estado
                TarjetaCRUD.actualizar_estado(tid, **kwargs)
                print("  Tarjeta actualizada.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "6":
            tid = input("ID tarjeta a eliminar: ").strip()
            if tid:
                try:
                    TarjetaCRUD.eliminar_tarjeta(tid)
                    print("  Tarjeta eliminada.")
                except Exception as e:
                    print(f"  Error: {e}")


def menu_usuarios():
    while True:
        print("\n--- Usuarios ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_usuarios()
        elif op == "2":
            uid = input("ID usuario: ").strip()
            if uid:
                try:
                    u = UsuarioCRUD.obtener_usuario(uid)
                    print(f"  {u}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            nombre = input("Nombre: ").strip()
            nombre_usuario = input("Nombre usuario: ").strip()
            email = input("Email: ").strip()
            contraseña = input("Contraseña: ").strip()
            if nombre and nombre_usuario and email and contraseña:
                try:
                    UsuarioCRUD.crear_usuario(nombre, nombre_usuario, email, contraseña)
                    print("  Usuario creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        elif op == "4":
            uid = input("ID usuario: ").strip()
            if not uid:
                continue
            nombre = input("Nombre (vacío=no cambiar): ").strip()
            email = input("Email (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if nombre:
                    kwargs["nombre"] = nombre
                if email:
                    kwargs["email"] = email
                UsuarioCRUD.actualizar_usuario(uid, **kwargs)
                print("  Usuario actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            uid = input("ID usuario a eliminar: ").strip()
            if uid:
                try:
                    UsuarioCRUD.eliminar_usuario(uid)
                    print("  Usuario eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")


def menu_usuariosApp():
    while True:
        print("\n--- Usuarios de la aplicación ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            UsuarioAppCRUD.obtener_usuarios()
        elif op == "2":
            uaid = input("ID usuario: ").strip()
            if uaid:
                try:
                    ua = UsuarioAppCRUD.obtener_usuario(uaid)
                    print(f"  {ua}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            username = input("Nombre de usuario: ").strip()
            contraseña_hash = input("Contraseña: ").strip()
            estado = input("Estado: ").strip()
            if username and contraseña_hash and estado:
                try:
                    UsuarioAppCRUD.crear_usuario(username, contraseña_hash, estado)
                    print("  Usuario creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        elif op == "4":
            uaid = input("ID usuario: ").strip()
            if not uaid:
                continue
            username = input("Nombre de usuario (vacío=no cambiar): ").strip()
            contraseña_hash = input("Contraseña (vacío=no cambiar): ").strip()
            estado = input("Estado (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if username:
                    kwargs["username"] = username
                if contraseña_hash:
                    kwargs["contraseña_hash"] = contraseña_hash
                if estado:
                    kwargs["estado"] = estado
                UsuarioAppCRUD.actualizar_usuario(uaid, **kwargs)
                print("  Usuario actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            uaid = input("ID usuario a eliminar: ").strip()
            if uaid:
                try:
                    UsuarioAppCRUD.eliminar_usuario(uaid)
                    print("  Usuario eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")


def _iniciar_api():
    """Ejecuta uvicorn en un hilo en segundo plano."""
    import uvicorn

    uvicorn.run("utils.app:app", host="127.0.0.1", port=8000, log_level="warning")


def main():
    print("API Banco - Menú por consola")
    print("Iniciando API en http://localhost:8000 ...")
    server = threading.Thread(target=_iniciar_api, daemon=True)
    server.start()
    time.sleep(1.5)
    print("API lista.\n")
    while True:
        print("\n========== MENÚ ==========")
        print(
            "1. Bancos  2. Clientes  3. Cuentas   4. Operaciones  5. Tarjetas   6. Usuarios de la aplicacion  7. Usuario"
        )
        op = input("Opción: ").strip()
        if op == "0":
            print("Hasta luego.")
            break
        if op == "1":
            menu_bancos()
        elif op == "2":
            menu_clientes()
        elif op == "3":
            menu_cuentas()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
