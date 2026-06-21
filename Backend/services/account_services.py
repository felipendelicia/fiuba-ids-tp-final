from Backend.db import execute
from Backend.dtos.errors import abort


def listar_usuarios(limit=10, offset=0):
    total = execute("SELECT COUNT(*) AS total FROM Accounts")[0]['total']
    usuarios = execute(f"SELECT * FROM Accounts LIMIT {limit} OFFSET {offset}")
    return usuarios, total


def obtener_cuenta(id):
    cuenta = execute(f"SELECT * FROM Accounts WHERE id = {id}")
    if not cuenta:
        abort(404, 'Usuario no encontrado')
    return cuenta[0]


def actualizar_usuario(id, username, email, password, phone, elo, is_active):
    cuenta = execute(f"SELECT id FROM Accounts WHERE id = {id}")
    if not cuenta:
        abort(404, 'Usuario no encontrado')
    execute(
        f"UPDATE Accounts SET username = '{username}', email = '{email}', "
        f"password = '{password}', phone = '{phone}', elo = '{elo}', "
        f"is_active = {is_active} WHERE id = '{id}'"
    )


def listar_reservas(id):
    pass


def actualizar_estado_usuario(id, is_active):
    cuenta = execute(f"SELECT id FROM Accounts WHERE id = {id}")
    if not cuenta:
        abort(404, 'Usuario no encontrado')
    execute(f"UPDATE Accounts SET is_active = {is_active} WHERE id = '{id}'")


def actualizar_genero_usuario(id, gender):
    cuenta = execute(f"SELECT id FROM Accounts WHERE id = {id}")
    if not cuenta:
        abort(404, 'Usuario no encontrado')
    execute(f"UPDATE Accounts SET gender = '{gender}' WHERE id = '{id}'")


def actualizar_password_usuario(id, password):
    cuenta = execute(f"SELECT id FROM Accounts WHERE id = {id}")
    if not cuenta:
        abort(404, 'Usuario no encontrado')
    execute(f"UPDATE Accounts SET password = '{password}' WHERE id = '{id}'")
