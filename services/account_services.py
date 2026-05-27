from db import execute


def listar_usuarios():
    usuarios_db = execute("SELECT * FROM Accounts") 
    if not usuarios_db:
        return None
    return usuarios_db


def obtener_cuenta(id):
    cuenta_id = execute(f'SELECT * FROM Accounts WHERE id = {id}')
    if not cuenta_id:
        return None
    return cuenta_id

def actualizar_usuario(id, username, email, password, phone, elo, is_active):
    cuenta_id = execute(f'SELECT * FROM Accounts WHERE id = {id}')
    if not cuenta_id:
        return None
    result = execute(f"UPDATE Accounts SET username = '{username}', email = '{email}', password = '{password}', phone = '{phone}', elo = '{elo}', is_active = {is_active} WHERE id = '{id}'")
    if result == False:
        return False
    return result

def listar_reservas(id):
    pass


def actualizar_estado_usuario(id, is_active):
    cuenta_id = execute(f"SELECT * FROM Accounts WHERE id = {id}")
    if not cuenta_id:
        return None
    cambio_estado = execute(f"UPDATE Accounts SET is_active = {is_active} WHERE id = '{id}'")
    if result == False:
        return False
    return result

def actualizar_genero_usuario(id):
    pass


def actualizar_password_usuario(id):
    pass
