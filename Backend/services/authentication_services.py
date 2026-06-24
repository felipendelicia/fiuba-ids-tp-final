from db import execute
from dtos.errors import abort


def login_usuario(email, password):
    result = execute(f"SELECT * FROM Accounts WHERE email = '{email}' AND password = '{password}' AND is_active = TRUE")
    if not result:
        abort(401, 'Credenciales invalidas')
    return result[0]


def registrar_usuario(name, username, email, password, dni, phone=None):
    conflict = execute(f"SELECT id FROM Accounts WHERE email = '{email}' OR username = '{username}' OR dni = '{dni}'")
    if conflict:
        abort(409, 'email, username o dni ya registrado')
    execute(
        f"INSERT INTO Accounts (name, username, email, password, dni, phone, created_at, updated_at) "
        f"VALUES ('{name}', '{username}', '{email}', '{password}', '{dni}', '{phone}', NOW(), NOW())"
    )
