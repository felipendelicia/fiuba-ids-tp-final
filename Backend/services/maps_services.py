from Backend.db import execute


def listar_mapas(limit, offset):
    total_result = execute("SELECT COUNT(*) as total FROM Maps")
    total = total_result[0]['total']

    mapas = execute(f"""
        SELECT id, name, image_url, description
        FROM Maps
        LIMIT {limit} OFFSET {offset}
    """)

    return mapas, total
