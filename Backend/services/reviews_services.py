from db import execute
from dtos.errors import abort


def listar_reviews(offset, limit, approved=None):
    where = ""
    if approved is not None:
        where = f"WHERE approved = {'TRUE' if approved else 'FALSE'}"
    total_result = execute(f"SELECT COUNT(*) as total FROM Review {where}")
    total = total_result[0]['total']
    reviews = execute(f"SELECT * FROM Review {where} LIMIT {limit} OFFSET {offset}")
    return reviews, total


def crear_map_review(stars, body_review, map_id, title=''):
    mapa = execute(f"SELECT id FROM Maps WHERE id = {map_id}")
    if not mapa:
        abort(404, 'Mapa no encontrado')
    body_sql = f"'{body_review}'" if body_review else "NULL"
    title_sql = f"'{title}'" if title else "NULL"
    execute(
        f"INSERT INTO Review (stars, title, body_review, map_id, created_at, approved) "
        f"VALUES ({stars}, {title_sql}, {body_sql}, {map_id}, CURDATE(), TRUE)"
    )


def actualizar_review(id, approved, admin_response=None):
    review = execute(f"SELECT id FROM Review WHERE id = {id}")
    if not review:
        abort(404, 'Reseña no encontrada')
    approved_val = 'TRUE' if approved else 'FALSE'
    if admin_response is not None:
        response_sql = f"'{admin_response}'"
        execute(f"UPDATE Review SET approved = {approved_val}, admin_response = {response_sql} WHERE id = {id}")
    else:
        execute(f"UPDATE Review SET approved = {approved_val} WHERE id = {id}")
