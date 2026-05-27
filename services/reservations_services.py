from db import execute


def listar_reservas(offset, limit, start_time, end_time, is_public):
    conditions= []
    params= []

    if start_time:
        conditions.append(f"start_time >= '{start_time}'")

    if end_time:
        conditions.append(f"end_time <= '{end_time}'")

    if is_public is not None:
        public_value= 0
        if is_public:
            public_value= 1
        conditions.append(f"is_public = {public_value}")

    where_clause= ""
    if condtions:
        where_clause= "WHERE " + " AND ".join(conditions)

    total_result= execute(f"SELECT COUNT(*) as total FROM Reservations {where_clause}")

    if total_result is False or not total_result:
        return None, None

    total = total_result[0]['total']
    reservations= execute(f"SELECT * FROM Reservations {where_clause} LIMIT {limit} OFFSET {offset}")

    if reservations is False:
        return None, None

    return reservations, total





def listar_reservas_usuario(offset, limit, id):
    total_result= execute(f"SELECT COUNT(*) as total FROM Reservations WHERE account_id = {id}")

    if total_result is False or not total_result:
        return None, None

    total= total_result[0]['total']
    reservations= execute(f"SELECT * FROM Reservations WHERE account_id = {id} LIMIT {limit} OFFSET {offset}")

    if reservations is False:
        return None, None

    return reservations, total



    


def crear_reserva(account_id, game_mode_id, map_id, equipment_kit_id, price, is_public, reservation_date, start_time, end_time, max_players):
    cupo= execute(f"""SELECT COUNT(id) as total_anotados FROM Reservations WHERE reservation_date = '{reservation_date}'
                    AND '{start_time}' < end_time AND '{end_time}' > start_time AND canceled = FALSE;""")

    if cupo:
        total_anotados= cupo[0]['total_anotados']
    else:
        total_anotados= 0

    #Valido que el usuario ya no se encuentre anotado en esta misma partida:
    query_usuario_duplicado= f"""SELECT id FROM Reservations WHERE account_id = {account_id}
                                AND reservation_date = '{reservation_date}' AND canceled = FALSE 
                                AND '{start_time}' < end_time AND '{end_time}' > start_time;"""

    if execute(query_usuario_duplicado):
        return False, "Ya tenés una reserva activa en este mismo rango horario"

    execute(f"""INSERT INTO Reservations
            (account_id, game_mode_id, map_id, created_at, equipment_kit_id, price, reservation_date, start_time, end_time, is_public)
            VALUES ({account_id}, {game_mode_id}, {map_id}, NOW(), {equipment_kit_id}, {price}, '{reservation_date}', '{start_time}', '{end_time}', {is_public});""")

    return True, None


def actualizar_reserva(id, data):
    campos= ['game_mode_id', 'map_id', 'equipment_kit_id', 'price', 
        'reservation_date', 'start_time', 'end_time', 
        'is_public', 'canceled', 'cancelation_reason']

    for key, value in data.items():
        if key in campos:
            if key in ['is_public', 'canceled']:
                if value is None:
                    updates.append(f"{key} = NULL")
                else:
                    boolean_value= 0
                    if value:
                        boolean_value= 1
                    updates.append(f"{key} = {boolean_value}")
                       
            else:
                if value is None:
                    updates.append(f"{key} = NULL")
                else:
                    updates.append(f"{key} = '{value}'")

    if not updates:
        return None

    set_clause = ", ".join(updates)

    check_exists = execute(f"SELECT * FROM Reservations WHERE id = {id}")
    if check_exists is False:
        return None

    if len(check_exists) == 0:
        return False  

    
    result = execute(f"UPDATE Reservations SET {set_clause} WHERE id = {id}")

    if result is False:
        return None

    return True

    

    

    


#def crear_public_reservation(id):




