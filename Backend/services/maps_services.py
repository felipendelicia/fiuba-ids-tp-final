from db import execute


def listar_mapas(limit, offset):
    total_result = execute("SELECT COUNT(*) as total FROM Maps")
    total = total_result[0]['total']

    mapas = execute(f"""
        SELECT id, name, vista_general_image_url, plano_despliegue_image_url, operaciones_terreno_image_url, description, capacity, extra_information, location, style, terrain, difficulty, compatible_gamemodes, origin, plano_image_url, zone_1_name, zone_1_description, zone_2_name, zone_2_description, zone_3_name, zone_3_description
        FROM Maps
        LIMIT {limit} OFFSET {offset}
    """)

    return mapas, total
