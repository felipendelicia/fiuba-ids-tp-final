from dtos.errors import abort


def validate_join_sala(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    required = ['account_id', 'equipment_kit_id']
    missing = [f for f in required if f not in data]
    if missing:
        abort(400, f'Campos requeridos: {", ".join(missing)}')
    return {
        'account_id': data['account_id'],
        'equipment_kit_id': data['equipment_kit_id'],
    }


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
        'sala_id': request.args.get('sala_id'),
    }


def validate_update_reservation(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    allowed = {'equipment_kit_id', 'canceled', 'cancelation_reason', 'account_id'}
    given = set(data.keys())
    invalid = given - allowed
    if invalid:
        abort(400, f'Campos invalidos: {", ".join(invalid)}')
    if not given:
        abort(400, 'Debe enviar al menos un campo a actualizar')
    return data


def _fmt_time(t):
    if t is None:
        return ''
    s = str(t)
    parts = s.split(':')
    if len(parts) == 3:
        return f'{int(parts[0]):02d}:{parts[1]}:{parts[2]}'
    return s


def build_reservation_response(r):
    return {
        'id': r['id'],
        'sala_id': r['sala_id'],
        'account_id': r['account_id'],
        'equipment_kit_id': r['equipment_kit_id'],
        'price': r.get('price', 0),
        'created_at': str(r.get('created_at', '')),
        'canceled': r.get('canceled', False),
        'cancelation_reason': r.get('cancelation_reason', ''),
    }
