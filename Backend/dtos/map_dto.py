from Backend.dtos.errors import abort


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
        'image_url': map_data.get('image_url', ''),
        'description': map_data.get('description', ''),
    }
