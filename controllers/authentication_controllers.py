from flask import request, jsonify
from flask_jwt_extended import create_access_token
from errors import ERRORS
from services.authentication_services import login_usuario as login_service
from services.authentication_services import registrar_usuario as registrar_service


def login_usuario():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return ERRORS['MISSING_REQUIRED_FIELDS']('email y password son requeridos')

    user = login_service(email, password)
    if not user:
        return ERRORS['NOT_FOUND']('Credenciales invalidas')

    token = create_access_token(identity=str(user['id']))
    return jsonify({'token': token, 'user_id': user['id']}), 200


def registrar_usuario():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    dni = data.get('dni')
    phone = data.get('phone')

    if not all([name, username, email, password, dni]):
        return ERRORS['MISSING_REQUIRED_FIELDS']('name, username, email, password y dni son requeridos')

    success, error = registrar_service(name, username, email, password, dni, phone)
    if error == 'conflict':
        return ERRORS['CONFLICT']('email, username o dni ya registrado')

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201
