from datetime import date
from db import execute


def listar_periodo_reservas(limit, offset, fecha=None):
    if not fecha:
        fecha = date.today().isoformat()
    count_result = execute(f"""
        SELECT COUNT(r.id) as total
        FROM Reservations r
        JOIN Salas s ON r.sala_id = s.id
        WHERE s.reservation_date = '{fecha}' AND r.canceled = FALSE
    """)
    total = count_result[0]['total'] if count_result else 0

    if total == 0:
        return [], 0

    reservas = execute(f"""
        SELECT r.id, r.price, s.start_time, s.end_time,
               a.name as user_name, a.dni as dni_usuario
        FROM Reservations r
        JOIN Accounts a ON r.account_id = a.id
        JOIN Salas s ON r.sala_id = s.id
        WHERE s.reservation_date = '{fecha}' AND r.canceled = FALSE
        LIMIT {limit} OFFSET {offset}
    """)
    return reservas, total


def get_dashboard_data(fecha, limit=100, offset=0):
    count_result = execute(f"""
        SELECT COUNT(r.id) as total
        FROM Reservations r
        JOIN Salas s ON r.sala_id = s.id
        WHERE s.reservation_date = '{fecha}' AND r.canceled = FALSE
    """)
    total = count_result[0]['total'] if count_result else 0

    reservas = []
    if total > 0:
        reservas = execute(f"""
            SELECT r.id,
                   r.price, s.start_time, s.end_time, s.map_id,
                   a.name as user_name, a.dni as dni_usuario,
                   m.name as map_name
            FROM Reservations r
            JOIN Accounts a ON r.account_id = a.id
            JOIN Salas s ON r.sala_id = s.id
            JOIN Maps m ON s.map_id = m.id
            WHERE s.reservation_date = '{fecha}' AND r.canceled = FALSE
            LIMIT {limit} OFFSET {offset}
        """)

    slots_raw = execute(f"""
        SELECT
            COALESCE(SUM(HOUR(s.start_time) = 5), 0) as cs,
            COALESCE(SUM(HOUR(s.start_time) = 7), 0) as so,
            COALESCE(SUM(HOUR(s.start_time) = 9), 0) as nd,
            COALESCE(SUM(HOUR(s.start_time) = 11), 0) as od,
            COALESCE(SUM(HOUR(s.start_time) = 13), 0) as tc,
            COALESCE(SUM(HOUR(s.start_time) = 15), 0) as qs,
            COALESCE(SUM(HOUR(s.start_time) = 17), 0) as do,
            COALESCE(SUM(HOUR(s.start_time) = 19), 0) as dv
        FROM Reservations r
        JOIN Salas s ON r.sala_id = s.id
        WHERE s.reservation_date = '{fecha}' AND r.canceled = FALSE
    """)

    frecuencia = dict(slots_raw[0]) if slots_raw else {'cs': 0, 'so': 0, 'nd': 0, 'od': 0, 'tc': 0, 'qs': 0, 'do': 0, 'dv': 0}

    ingresos = {'dia': 0, 'semana': 0, 'mes': 0, 'año': 0}

    dia_data = execute(f"SELECT COALESCE(SUM(r.price), 0) as total FROM Reservations r JOIN Salas s ON r.sala_id = s.id WHERE s.reservation_date = '{fecha}' AND r.canceled = FALSE")
    if dia_data:
        ingresos['dia'] = int(dia_data[0]['total'])

    semana_data = execute(f"SELECT COALESCE(SUM(r.price), 0) as total FROM Reservations r JOIN Salas s ON r.sala_id = s.id WHERE YEARWEEK(s.reservation_date, 1) = YEARWEEK('{fecha}', 1) AND r.canceled = FALSE")
    if semana_data:
        ingresos['semana'] = int(semana_data[0]['total'])

    mes_data = execute(f"SELECT COALESCE(SUM(r.price), 0) as total FROM Reservations r JOIN Salas s ON r.sala_id = s.id WHERE MONTH(s.reservation_date) = MONTH('{fecha}') AND YEAR(s.reservation_date) = YEAR('{fecha}') AND r.canceled = FALSE")
    if mes_data:
        ingresos['mes'] = int(mes_data[0]['total'])

    anio_data = execute(f"SELECT COALESCE(SUM(r.price), 0) as total FROM Reservations r JOIN Salas s ON r.sala_id = s.id WHERE YEAR(s.reservation_date) = YEAR('{fecha}') AND r.canceled = FALSE")
    if anio_data:
        ingresos['año'] = int(anio_data[0]['total'])

    cap_result = execute(f"""
        SELECT COALESCE(SUM(max_players), 0) as total
        FROM Salas
        WHERE reservation_date = '{fecha}' AND canceled = FALSE
    """)
    total_capacidad = int(cap_result[0]['total']) if cap_result else 0

    return reservas, frecuencia, ingresos, total, total_capacidad
