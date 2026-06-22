from dtos.errors import abort


def validate_list_maps(request):
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        abort(400, '_limit y _offset deben ser enteros')
    if limit < 1 or offset < 0:
        abort(400, '_limit debe ser >= 1 y _offset >= 0')
    return {'limit': limit, 'offset': offset}


def build_map_response(map_data):
    return {
        'id': map_data['id'],
        'name': map_data['name'],
        'vista_general_image_url': map_data.get('vista_general_image_url', ''),
        'plano_despliegue_image_url': map_data.get('plano_despliegue_image_url', ''),
        'operaciones_terreno_image_url': map_data.get('operaciones_terreno_image_url', ''),
        'description': map_data.get('description', ''),
        'capacity': map_data.get('capacity', ''),
        'extra_information': map_data.get('extra_information', ''),
        'location': map_data.get('location', ''),
        'style': map_data.get('style', ''),
        'terrain': map_data.get('terrain', ''),
        'difficulty': map_data.get('difficulty', ''),
        'compatible_gamemodes': map_data.get('compatible_gamemodes', ''),
        'origin': map_data.get('origin', ''),
        'plano_image_url': map_data.get('plano_image_url', ''),
        'zone_1_name': map_data.get('zone_1_name', ''),
        'zone_1_description': map_data.get('zone_1_description', ''),
        'zone_2_name': map_data.get('zone_2_name', ''),
        'zone_2_description': map_data.get('zone_2_description', ''),
        'zone_3_name': map_data.get('zone_3_name', ''),
        'zone_3_description': map_data.get('zone_3_description', ''),
    }
