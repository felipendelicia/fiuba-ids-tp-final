from dtos.errors import abort


def validate_login(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        abort(400, 'email y password son requeridos')
    return {'email': email.strip(), 'password': password}


def validate_register(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    dni = data.get('dni')
    phone = data.get('phone')
    if not all([name, username, email, password, dni]):
        abort(400, 'name, username, email, password y dni son requeridos')
    return {
        'name': name.strip(),
        'username': username.strip(),
        'email': email.strip(),
        'password': password,
        'dni': str(dni).strip(),
        'phone': phone.strip() if phone else None,
    }
