from db import execute


def listar_mapas(limit, offset):
    total_result = execute("SELECT COUNT(*) as total FROM Maps")
    total = total_result[0]['total']

    mapas = execute(f"""
        SELECT id, name, vista_general_image_url, plano_despliegue_image_url, operaciones_terreno_image_url, description, capacity, extra_information, location, style, terrain, difficulty, compatible_gamemodes
        FROM Maps
        LIMIT {limit} OFFSET {offset}
    """)

    return mapas, total
