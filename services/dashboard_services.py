from datetime import date
from db import execute


def listar_periodo_reservas(limit, offset):
    today = date.today().isoformat()
    count_result = execute(f"SELECT COUNT(r.id) as total FROM Reservations r WHERE r.reservation_date = '{today}' AND r.canceled = FALSE")
    total = count_result[0]['total']

    if total == 0:
        return [], 0

    reservas = execute(f"""
        SELECT r.id, r.price, r.start_time, r.end_time,
               a.name as user_name, a.dni as dni_usuario
        FROM Reservations r
        JOIN Accounts a ON r.account_id = a.id
        WHERE r.reservation_date = '{today}' AND r.canceled = FALSE
        LIMIT {limit} OFFSET {offset}
    """)
    return reservas, total
