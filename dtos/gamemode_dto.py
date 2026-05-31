from dtos.errors import abort


def validate_create_gamemode(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    name = data.get('name')
    duration = data.get('duration')
    players = data.get('players')
    if not name or not duration or players is None:
        abort(400, 'Campos requeridos: name, duration, players')
    return {
        'name': name.strip(),
        'duration': str(duration).strip(),
        'players': int(players),
    }


validate_replace_gamemode = validate_create_gamemode


def build_gamemode_response(gm):
    return {
        'id': gm['id'],
        'name': gm['name'],
        'duration': gm['duration'],
        'players': gm['players'],
    }
