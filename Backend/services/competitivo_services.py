from db import execute
from dtos.errors import abort


def listar_eventos(offset=0, limit=100):
    total_result = execute("SELECT COUNT(*) as total FROM CompetitivoEvent")
    total = total_result[0]['total']
    eventos = execute(f"SELECT * FROM CompetitivoEvent ORDER BY sort_order ASC LIMIT {limit} OFFSET {offset}")
    return eventos, total


def obtener_evento(id):
    rows = execute(f"SELECT * FROM CompetitivoEvent WHERE id = {id}")
    if not rows:
        abort(404, 'Evento no encontrado')
    return rows[0]


def crear_evento(title, description=None, image_url=None, badge=None, event_date=None, event_time=None):
    desc_sql = f"'{description}'" if description else "NULL"
    img_sql = f"'{image_url}'" if image_url else "NULL"
    badge_sql = f"'{badge}'" if badge else "NULL"
    date_sql = f"'{event_date}'" if event_date else "NULL"
    time_sql = f"'{event_time}'" if event_time else "NULL"
    execute(
        f"INSERT INTO CompetitivoEvent (title, description, image_url, badge, event_date, event_time) "
        f"VALUES ('{title}', {desc_sql}, {img_sql}, {badge_sql}, {date_sql}, {time_sql})"
    )


def reemplazar_evento(id, title, description=None, image_url=None, badge=None, event_date=None, event_time=None):
    evento = execute(f"SELECT id FROM CompetitivoEvent WHERE id = {id}")
    if not evento:
        abort(404, 'Evento no encontrado')
    desc_sql = f"'{description}'" if description else "NULL"
    img_sql = f"'{image_url}'" if image_url else "NULL"
    badge_sql = f"'{badge}'" if badge else "NULL"
    date_sql = f"'{event_date}'" if event_date else "NULL"
    time_sql = f"'{event_time}'" if event_time else "NULL"
    execute(
        f"UPDATE CompetitivoEvent SET title = '{title}', description = {desc_sql}, "
        f"image_url = {img_sql}, badge = {badge_sql}, "
        f"event_date = {date_sql}, event_time = {time_sql} "
        f"WHERE id = {id}"
    )


def eliminar_evento(id):
    evento = execute(f"SELECT id FROM CompetitivoEvent WHERE id = {id}")
    if not evento:
        abort(404, 'Evento no encontrado')
    execute(f"DELETE FROM CompetitivoEvent WHERE id = {id}")