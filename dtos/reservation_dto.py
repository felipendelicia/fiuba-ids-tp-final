from dtos.errors import abort


def validate_list_reservations(request):
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        abort(400, '_limit y _offset deben ser enteros')
    if limit < 1 or offset < 0:
        abort(400, '_limit >= 1 y _offset >= 0')
    return {
        'limit': limit,
        'offset': offset,
        'start_time': request.args.get('start_time'),
        'end_time': request.args.get('end_time'),
        'is_public': request.args.get('is_public'),
    }


def validate_list_user_reservations(request):
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        abort(400, '_limit y _offset deben ser enteros')
    if limit < 1 or offset < 0:
        abort(400, '_limit >= 1 y _offset >= 0')
    return {'limit': limit, 'offset': offset}


def validate_create_reservation(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    required = ['account_id', 'map_id', 'equipment_kit_id', 'price', 'reservation_date', 'start_time', 'end_time']
    missing = [f for f in required if f not in data]
    if missing:
        abort(400, f'Campos requeridos: {", ".join(missing)}')
    return {k: data[k] for k in required}


def validate_create_public_reservation(request):
    return validate_create_reservation(request)


def validate_update_reservation(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    allowed = {'game_mode_id', 'map_id', 'equipment_kit_id', 'price',
               'reservation_date', 'start_time', 'end_time',
               'is_public', 'canceled', 'cancelation_reason'}
    given = set(data.keys())
    invalid = given - allowed
    if invalid:
        abort(400, f'Campos inválidos: {", ".join(invalid)}')
    if not given:
        abort(400, 'Debe enviar al menos un campo a actualizar')
    return data


def build_reservation_response(res):
    return {
        'id': res['id'],
        'account_id': res['account_id'],
        'game_mode_id': res['game_mode_id'],
        'map_id': res['map_id'],
        'equipment_kit_id': res['equipment_kit_id'],
        'price': res['price'],
        'reservation_date': str(res.get('reservation_date', '')),
        'start_time': str(res.get('start_time', '')),
        'end_time': str(res.get('end_time', '')),
        'is_public': res.get('is_public', False),
        'canceled': res.get('canceled', False),
        'cancelation_reason': res.get('cancelation_reason', ''),
        'created_at': str(res.get('created_at', '')),
    }
