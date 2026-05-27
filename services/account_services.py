from db import execute


def listar_usuarios():
    usuarios_db = execute(f"SELECT * FROM Accounts") 
    if not usuarios_db:
        return None
    return usuarios_db


def obtener_cuenta(id):
    cuenta_id = execute(f'SELECT * FROM Accounts WHERE id = {id}')
    if not cuenta_id:
        return None
    return cuenta_id


def actualizar_usuario(id):
    pass


def listar_reservas(id):
    pass


def actualizar_estado_usuario(id):
    pass


def actualizar_genero_usuario(id):
    pass


def actualizar_password_usuario(id):
    pass
