from Backend.dtos.errors import abort


def validate_list_reviews(request):
    try:
        offset = int(request.args.get('_offset', 0))
        limit = int(request.args.get('_limit', 10))
    except ValueError:
        abort(400, '_offset y _limit deben ser enteros')
    if offset < 0 or limit < 1:
        abort(400, '_offset >= 0 y _limit >= 1')
    approved = request.args.get('approved')
    approved_val = None
    if approved is not None:
        approved_val = approved.lower() == 'true'
    return {'offset': offset, 'limit': limit, 'approved': approved_val}


def validate_create_review(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    stars = data.get('stars')
    map_id = data.get('map_id')
    if stars is None or map_id is None:
        abort(400, 'stars y map_id son requeridos')
    if not isinstance(stars, int) or stars < 1 or stars > 5:
        abort(400, 'stars debe ser un entero entre 1 y 5')
    if not isinstance(map_id, int) or map_id < 1:
        abort(400, 'map_id debe ser un entero positivo')
    return {
        'stars': stars,
        'map_id': map_id,
        'body_review': data.get('body_review', '').strip()
    }


def validate_update_review(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    approved = data.get('approved')
    if approved is None:
        abort(400, 'approved es requerido')
    if not isinstance(approved, bool):
        abort(400, 'approved debe ser un booleano')
    return {'approved': approved}


def build_review_response(review):
    return {
        'id': review['id'],
        'stars': review['stars'],
        'body_review': review.get('body_review', ''),
        'map_id': review['map_id'],
        'created_at': str(review.get('created_at', '')),
        'approved': review.get('approved', False)
    }
