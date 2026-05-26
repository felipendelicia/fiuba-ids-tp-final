from db import execute


def listar_reviews(offset, limit):
    total_result = execute("SELECT COUNT(*) as total FROM Review")
    if total_result is False:
        return None, None
    total = total_result[0]['total']
    reviews = execute(f"SELECT * FROM Review LIMIT {limit} OFFSET {offset}")
    if reviews is False:
        return None, None
    return reviews, total


def crear_map_review(stars, body_review, map_id):
    mapa = execute(f"SELECT id FROM Maps WHERE id = {map_id}")
    if not mapa:
        return None, 'not_found'
    body_sql = f"'{body_review}'" if body_review else "NULL"
    execute(
        f"INSERT INTO Review (stars, body_review, map_id, created_at, approved) "
        f"VALUES ({stars}, {body_sql}, {map_id}, CURDATE(), FALSE)"
    )
    return True, None


def actualizar_review(id, approved):
    review = execute(f"SELECT id FROM Review WHERE id = {id}")
    if not review:
        return None, 'not_found'
    approved_val = 'TRUE' if approved else 'FALSE'
    execute(f"UPDATE Review SET approved = {approved_val} WHERE id = {id}")
    return True, None
