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


import re


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
    dni_str = str(dni).strip()
    if not re.match(r'^\d{7,8}$', dni_str):
        abort(400, 'DNI debe ser un número de 7 u 8 dígitos, sin puntos ni guiones')
    phone_str = phone.strip() if phone else None
    if phone_str is not None and not re.match(r'^\+?\d{7,15}$', phone_str.replace(' ', '').replace('-', '')):
        abort(400, 'Teléfono inválido: debe contener entre 7 y 15 dígitos')
    return {
        'name': name.strip(),
        'username': username.strip(),
        'email': email.strip(),
        'password': password,
        'dni': dni_str,
        'phone': phone_str,
    }
