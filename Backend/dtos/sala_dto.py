from dtos.errors import abort


def validate_create_sala(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    required = ['game_mode_id', 'map_id', 'price',
                'reservation_date', 'start_time', 'end_time', 'max_players', 'admin_account_id']
    missing = [f for f in required if f not in data]
    if missing:
        abort(400, f'Campos requeridos: {", ".join(missing)}')
    validate_sala_time(data['start_time'], data['end_time'])
    dto = {k: data[k] for k in required}
    if 'equipment_kit_id' in data:
        dto['equipment_kit_id'] = data['equipment_kit_id']
    return dto


def validate_list_salas(request):
    try:
        limit = int(request.args.get('_limit', 50))
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
        'reservation_date': request.args.get('reservation_date'),
    }


def validate_update_sala(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    allowed = {'game_mode_id', 'map_id', 'equipment_kit_id', 'price',
               'reservation_date', 'start_time', 'end_time',
               'max_players', 'canceled', 'cancelation_reason', 'admin_account_id'}
    given = set(data.keys())
    invalid = given - allowed
    if invalid:
        abort(400, f'Campos inválidos: {", ".join(invalid)}')
    if not given:
        abort(400, 'Debe enviar al menos un campo a actualizar')
    if 'start_time' in data or 'end_time' in data:
        validate_sala_time(data.get('start_time'), data.get('end_time'))
    return data


def _fmt_time(t):
    if t is None:
        return ''
    s = str(t)
    parts = s.split(':')
    if len(parts) == 3:
        return f'{int(parts[0]):02d}:{parts[1]}:{parts[2]}'
    return s


def build_sala_response(s):
    return {
        'id': s['id'],
        'game_mode_id': s['game_mode_id'],
        'map_id': s['map_id'],
        'equipment_kit_id': s.get('equipment_kit_id'),
        'price': s['price'],
        'reservation_date': str(s.get('reservation_date', '')),
        'start_time': _fmt_time(s.get('start_time')),
        'end_time': _fmt_time(s.get('end_time')),
        'max_players': s['max_players'],
        'current_players': s.get('current_players', 0),
        'admin_account_id': s['admin_account_id'],
        'is_public': s.get('is_public', True),
        'created_at': str(s.get('created_at', '')),
        'canceled': s.get('canceled', False),
        'cancelation_reason': s.get('cancelation_reason', ''),
    }


def validate_sala_time(start_time, end_time):
    SLOT_STARTS = ['05:00:00','07:00:00','09:00:00','11:00:00',
                   '13:00:00','15:00:00','17:00:00','19:00:00']
    if start_time not in SLOT_STARTS:
        abort(400, f'Horario inválido. Debe ser uno de: {", ".join(SLOT_STARTS)}')
    try:
        hora = int(start_time.split(':')[0])
        expected_end = f'{hora + 2:02d}:00:00'
    except (ValueError, IndexError):
        abort(400, 'Formato de hora de inicio inválido')
    if end_time != expected_end:
        abort(400, 'La reserva debe ser de exactamente 2 horas')
