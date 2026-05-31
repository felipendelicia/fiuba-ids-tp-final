from db import execute
from dtos.errors import abort


def listar_reservas(params):
    offset = params['offset']
    limit = params['limit']
    start_time = params.get('start_time')
    end_time = params.get('end_time')
    is_public = params.get('is_public')

    conditions = []

    if start_time:
        conditions.append(f"start_time >= '{start_time}'")

    if end_time:
        conditions.append(f"end_time <= '{end_time}'")

    if is_public is not None:
        public_value = 1 if is_public else 0
        conditions.append(f"is_public = {public_value}")

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    total_result = execute(f"SELECT COUNT(*) as total FROM Reservations {where_clause}")
    total = total_result[0]['total']
    reservations = execute(f"SELECT * FROM Reservations {where_clause} LIMIT {limit} OFFSET {offset}")
    return reservations, total


def listar_reservas_usuario(params, id):
    offset = params['offset']
    limit = params['limit']

    total_result = execute(f"SELECT COUNT(*) as total FROM Reservations WHERE account_id = {id}")
    total = total_result[0]['total']
    reservations = execute(f"SELECT * FROM Reservations WHERE account_id = {id} LIMIT {limit} OFFSET {offset}")
    return reservations, total


def crear_reserva(params):
    account_id = params['account_id']
    game_mode_id = params['game_mode_id']
    map_id = params['map_id']
    equipment_kit_id = params['equipment_kit_id']
    price = params['price']
    is_public = params['is_public']
    reservation_date = params['reservation_date']
    start_time = params['start_time']
    end_time = params['end_time']

    game_mode = execute(f"SELECT * FROM GameModes WHERE id = {game_mode_id}")
    if not game_mode:
        abort(404, 'Modo de juego no encontrado')

    cupo = execute(f"""SELECT COUNT(id) as total_anotados FROM Reservations
                    WHERE reservation_date = '{reservation_date}'
                    AND '{start_time}' < end_time AND '{end_time}' > start_time
                    AND canceled = FALSE""")
    total_anotados = cupo[0]['total_anotados'] if cupo else 0

    duplicado = execute(f"""SELECT id FROM Reservations WHERE account_id = {account_id}
                        AND reservation_date = '{reservation_date}' AND canceled = FALSE
                        AND '{start_time}' < end_time AND '{end_time}' > start_time""")
    if duplicado:
        abort(409, 'Ya tenés una reserva activa en este mismo rango horario')

    execute(f"""INSERT INTO Reservations
            (account_id, game_mode_id, map_id, created_at, equipment_kit_id, price, reservation_date, start_time, end_time, is_public)
            VALUES ({account_id}, {game_mode_id}, {map_id}, NOW(), {equipment_kit_id}, {price}, '{reservation_date}', '{start_time}', '{end_time}', {is_public})""")

    user = execute(f"SELECT email FROM Accounts WHERE id = {account_id}")
    if not user:
        abort(404, 'Usuario no encontrado')
    return user[0]['email']


def actualizar_reserva(id, data):
    updates = []
    campos = ['game_mode_id', 'map_id', 'equipment_kit_id', 'price',
              'reservation_date', 'start_time', 'end_time',
              'is_public', 'canceled', 'cancelation_reason']

    for key, value in data.items():
        if key in campos:
            if key in ('is_public', 'canceled'):
                if value is None:
                    updates.append(f"{key} = NULL")
                else:
                    updates.append(f"{key} = {1 if value else 0}")
            else:
                if value is None:
                    updates.append(f"{key} = NULL")
                else:
                    updates.append(f"{key} = '{value}'")

    if not updates:
        abort(400, 'No hay campos válidos para actualizar')

    check = execute(f"SELECT id FROM Reservations WHERE id = {id}")
    if not check:
        abort(404, f'Reserva con ID {id} no encontrada')

    set_clause = ", ".join(updates)
    execute(f"UPDATE Reservations SET {set_clause} WHERE id = {id}")
