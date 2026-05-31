from dtos.errors import abort


def validate_update_user(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    required = ['username', 'email', 'password', 'phone', 'elo', 'is_active']
    missing = [f for f in required if f not in data]
    if missing:
        abort(400, f'Campos requeridos: {", ".join(missing)}')
    return {
        'username': data['username'],
        'email': data['email'],
        'password': data['password'],
        'phone': data['phone'],
        'elo': data['elo'],
        'is_active': data['is_active'],
    }


def validate_toggle_status(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    if 'is_active' not in data:
        abort(400, 'Campo requerido: is_active')
    return {'is_active': data['is_active']}


def validate_update_gender(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    if 'gender' not in data:
        abort(400, 'Campo requerido: gender')
    return {'gender': data['gender']}


def validate_update_password(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    if 'password' not in data:
        abort(400, 'Campo requerido: password')
    return {'password': data['password']}


def build_user_response(user):
    return {
        'id': user['id'],
        'name': user['name'],
        'username': user['username'],
        'email': user['email'],
        'dni': user['dni'],
        'phone': user.get('phone', ''),
        'gender': user.get('gender', ''),
        'about_me': user.get('about_me', ''),
        'is_active': user.get('is_active', False),
        'is_admin': user.get('is_admin', False),
        'elo': user.get('elo', 0),
        'created_at': str(user.get('created_at', '')),
        'updated_at': str(user.get('updated_at', '')),
    }
