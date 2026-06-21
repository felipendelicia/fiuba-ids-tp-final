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


def crear_map_review(stars, body_review, map_id):
    mapa = execute(f"SELECT id FROM Maps WHERE id = {map_id}")
    if not mapa:
        abort(404, 'Mapa no encontrado')
    body_sql = f"'{body_review}'" if body_review else "NULL"
    execute(
        f"INSERT INTO Review (stars, body_review, map_id, created_at, approved) "
        f"VALUES ({stars}, {body_sql}, {map_id}, CURDATE(), FALSE)"
    )


def actualizar_review(id, approved):
    review = execute(f"SELECT id FROM Review WHERE id = {id}")
    if not review:
        abort(404, 'Reseña no encontrada')
    approved_val = 'TRUE' if approved else 'FALSE'
    execute(f"UPDATE Review SET approved = {approved_val} WHERE id = {id}")
