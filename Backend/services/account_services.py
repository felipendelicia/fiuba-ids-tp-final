from db import execute
from dtos.errors import abort


def listar_usuarios(limit=10, offset=0):
    total = execute("SELECT COUNT(*) AS total FROM Accounts")[0]['total']
    usuarios = execute(f"SELECT * FROM Accounts LIMIT {limit} OFFSET {offset}")
    return usuarios, total


def obtener_cuenta(id):
    cuenta = execute(f"SELECT * FROM Accounts WHERE id = {id}")
    if not cuenta:
        abort(404, 'Usuario no encontrado')
    user = cuenta[0]
    count = execute(f"""
        SELECT COUNT(DISTINCT s.id) as cnt
        FROM Salas s
        LEFT JOIN Reservations r ON r.sala_id = s.id AND r.account_id = {id} AND r.canceled = FALSE
        WHERE (s.admin_account_id = {id} OR r.id IS NOT NULL) AND s.canceled = FALSE
    """)
    user['played_games'] = count[0]['cnt'] if count else 0
    hours = execute(f"""
        SELECT COALESCE(SUM(TIMESTAMPDIFF(HOUR, s.start_time, s.end_time)), 0) as total
        FROM Salas s
        LEFT JOIN Reservations r ON r.sala_id = s.id AND r.account_id = {id} AND r.canceled = FALSE
        WHERE (s.admin_account_id = {id} OR r.id IS NOT NULL) AND s.canceled = FALSE
    """)
    user['hours_played'] = int(hours[0]['total']) if hours else 0
    return user


def actualizar_usuario(id, **kwargs):
    cuenta = execute(f"SELECT id FROM Accounts WHERE id = {id}")
    if not cuenta:
        abort(404, 'Usuario no encontrado')
    if not kwargs:
        abort(400, 'No hay campos para actualizar')
    set_parts = []
    for key, value in kwargs.items():
        if key in ('is_active',):
            set_parts.append(f"{key} = {1 if value else 0}")
        else:
            set_parts.append(f"{key} = '{value}'")
    set_clause = ", ".join(set_parts)
    execute(f"UPDATE Accounts SET {set_clause} WHERE id = '{id}'")


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
