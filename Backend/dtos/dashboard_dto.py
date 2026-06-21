from Backend.dtos.errors import abort


def validate_disponibility(request):
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        abort(400, '_limit y _offset deben ser enteros')
    if limit < 1 or offset < 0:
        abort(400, '_limit >= 1 y _offset >= 0')
    return {'limit': limit, 'offset': offset}
