from db import execute, get_db_connection
from dtos.errors import abort


def listar_salas(params):
    offset = params['offset']
    limit = params['limit']
    start_time = params.get('start_time')
    end_time = params.get('end_time')
    is_public = params.get('is_public')
    reservation_date = params.get('reservation_date')

    conditions = ['s.canceled = FALSE']

    if start_time:
        conditions.append(f"s.start_time >= '{start_time}'")
    if end_time:
        conditions.append(f"s.end_time <= '{end_time}'")
    if is_public is not None:
        conditions.append(f"s.is_public = {1 if is_public else 0}")
    if reservation_date:
        conditions.append(f"s.reservation_date = '{reservation_date}'")

    where = "WHERE " + " AND ".join(conditions)

    total_result = execute(f"SELECT COUNT(*) as total FROM Salas s {where}")
    total = total_result[0]['total']

    salas = execute(f"""SELECT s.*,
        (SELECT COUNT(*) FROM Reservations r WHERE r.sala_id = s.id AND r.canceled = FALSE) as current_players
        FROM Salas s {where} ORDER BY s.reservation_date, s.start_time LIMIT {limit} OFFSET {offset}""")

    return salas, total


def crear_sala(params):
    game_mode_id = params['game_mode_id']
    map_id = params['map_id']
    equipment_kit_id = params.get('equipment_kit_id')
    price = params['price']
    reservation_date = params['reservation_date']
    start_time = params['start_time']
    end_time = params['end_time']
    max_players = params['max_players']
    admin_account_id = params['admin_account_id']
    account_id = params.get('account_id')
    join_kit_id = params.get('join_equipment_kit_id')

    game_mode = execute(f"SELECT * FROM GameModes WHERE id = {game_mode_id}")
    if not game_mode:
        abort(404, 'Modo de juego no encontrado')

    mapa = execute(f"SELECT * FROM Maps WHERE id = {map_id}")
    if not mapa:
        abort(404, 'Mapa no encontrado')

    kit_val = f"'{equipment_kit_id}'" if equipment_kit_id else "NULL"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute(f"""INSERT INTO Salas
            (game_mode_id, map_id, equipment_kit_id, price, reservation_date, start_time, end_time, max_players, admin_account_id)
            VALUES ({game_mode_id}, {map_id}, {kit_val}, {price}, '{reservation_date}', '{start_time}', '{end_time}', {max_players}, {admin_account_id})""")
        sala_id = cursor.lastrowid

        if account_id:
            if not join_kit_id:
                abort(400, 'join_equipment_kit_id requerido para unirse a la sala')

            current = execute(f"SELECT COUNT(*) as cnt FROM Reservations WHERE sala_id = {sala_id} AND canceled = FALSE")
            if current[0]['cnt'] >= max_players:
                abort(409, 'La sala está completa')

            duplicado = execute(f"SELECT id FROM Reservations WHERE sala_id = {sala_id} AND account_id = {account_id} AND canceled = FALSE")
            if duplicado:
                abort(409, 'Ya estás registrado en esta sala')

            kit = execute(f"SELECT price FROM EquipmentKit WHERE id = {join_kit_id}")
            kit_price = kit[0]['price'] if kit else 0
            total_price = int(price) + int(kit_price)

            cursor.execute(f"""INSERT INTO Reservations (sala_id, account_id, equipment_kit_id, price)
                    VALUES ({sala_id}, {account_id}, {join_kit_id}, {total_price})""")

        conn.commit()

        if account_id:
            user = execute(f"SELECT email FROM Accounts WHERE id = {account_id}")
            if user:
                return user[0]['email']

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def actualizar_sala(id, data):
    updates = []
    campos = ['game_mode_id', 'map_id', 'equipment_kit_id', 'price',
              'reservation_date', 'start_time', 'end_time',
              'max_players', 'canceled', 'cancelation_reason']

    for key, value in data.items():
        if key in campos:
            if key in ('canceled',):
                updates.append(f"{key} = {1 if value else 0}")
            else:
                updates.append(f"{key} = '{value}'")

    if not updates:
        abort(400, 'No hay campos válidos para actualizar')

    check = execute(f"SELECT * FROM Salas WHERE id = {id}")
    if not check:
        abort(404, f'Sala con ID {id} no encontrada')
    sala = check[0]

    if data.get('canceled') and data.get('admin_account_id') is not None:
        if sala['admin_account_id'] != data['admin_account_id']:
            abort(403, 'Solo el admin que creó la sala puede cancelarla')

    set_clause = ", ".join(updates)
    execute(f"UPDATE Salas SET {set_clause} WHERE id = {id}")

    if data.get('canceled'):
        execute(f"UPDATE Reservations SET canceled = 1, cancelation_reason = 'Sala cancelada por el administrador' WHERE sala_id = {id} AND canceled = FALSE")
