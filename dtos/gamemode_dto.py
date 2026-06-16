from dtos.errors import abort


def validate_create_gamemode(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    name = data.get('name')
    duration = data.get('duration')
    players = data.get('players')
    description = data.get('description')
    if not name or not duration or players is None or not description:
        abort(400, 'Campos requeridos: name, duration, players, description')
    if str(duration).strip() not in {'30', '60', '90', '120'}:
        abort(400, 'Duración inválida. Valores permitidos: 30, 60, 90, 120')
    return {
        'name': name.strip(),
        'duration': str(duration).strip(),
        'players': int(players),
        'description': description.strip(),
    }


validate_replace_gamemode = validate_create_gamemode


def build_gamemode_response(gm):
    return {
        'id': gm['id'],
        'name': gm['name'],
        'duration': gm['duration'],
        'players': gm['players'],
        'description': gm['description'],
        'maps': gm['maps'],
    }
