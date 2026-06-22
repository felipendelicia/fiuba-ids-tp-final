from db import execute
from dtos.errors import abort


def listar_reservas(params):
    offset = params['offset']
    limit = params['limit']
    sala_id = params.get('sala_id')

    conditions = ['r.canceled = FALSE']
    if sala_id:
        conditions.append(f"r.sala_id = {sala_id}")

    where = "WHERE " + " AND ".join(conditions)

    total_result = execute(f"SELECT COUNT(*) as total FROM Reservations r {where}")
    total = total_result[0]['total']
    reservations = execute(f"SELECT r.* FROM Reservations r {where} LIMIT {limit} OFFSET {offset}")
    return reservations, total


def crear_reserva(sala_id, params):
    account_id = params['account_id']
    equipment_kit_id = params['equipment_kit_id']

    sala = execute(f"SELECT * FROM Salas WHERE id = {sala_id}")
    if not sala:
        abort(404, 'Sala no encontrada')
    sala = sala[0]

    if sala['canceled']:
        abort(400, 'La sala está cancelada')

    current = execute(f"SELECT COUNT(*) as cnt FROM Reservations WHERE sala_id = {sala_id} AND canceled = FALSE")
    if current[0]['cnt'] >= sala['max_players']:
        abort(409, 'La sala está completa')

    duplicado = execute(f"SELECT id FROM Reservations WHERE sala_id = {sala_id} AND account_id = {account_id} AND canceled = FALSE")
    if duplicado:
        abort(409, 'Ya estás registrado en esta sala')

    kit = execute(f"SELECT price FROM EquipmentKit WHERE id = {equipment_kit_id}")
    kit_price = kit[0]['price'] if kit else 0
    total_price = int(sala['price']) + int(kit_price)

    existing = execute(f"SELECT id FROM Reservations WHERE sala_id = {sala_id} AND account_id = {account_id} AND canceled = TRUE")
    if existing:
        execute(f"""UPDATE Reservations SET canceled = FALSE, equipment_kit_id = {equipment_kit_id}, price = {total_price}
                WHERE id = {existing[0]['id']}""")
    else:
        execute(f"""INSERT INTO Reservations (sala_id, account_id, equipment_kit_id, price)
                VALUES ({sala_id}, {account_id}, {equipment_kit_id}, {total_price})""")

    user = execute(f"SELECT email FROM Accounts WHERE id = {account_id}")
    if not user:
        abort(404, 'Usuario no encontrado')
    return user[0]['email']


def actualizar_reserva(id, data):
    updates = []
    campos = ['equipment_kit_id', 'canceled', 'cancelation_reason']

    for key, value in data.items():
        if key in campos:
            if key == 'canceled':
                updates.append(f"{key} = {1 if value else 0}")
            else:
                if value is None:
                    updates.append(f"{key} = NULL")
                else:
                    updates.append(f"{key} = '{value}'")

    if not updates:
        abort(400, 'No hay campos válidos para actualizar')

    check = execute(f"SELECT * FROM Reservations WHERE id = {id}")
    if not check:
        abort(404, f'Reserva con ID {id} no encontrada')

    current = check[0]
    if data.get('account_id') is not None and current['account_id'] != data['account_id']:
        abort(403, 'No puedes modificar una reserva que no te pertenece')

    set_clause = ", ".join(updates)
    execute(f"UPDATE Reservations SET {set_clause} WHERE id = {id}")
