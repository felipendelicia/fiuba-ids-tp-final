from flask import g, jsonify
from flask_jwt_extended import create_access_token
from Backend.dtos.errors import validate_dto
from Backend.dtos.auth_dto import validate_login, validate_register
from Backend.services.authentication_services import login_usuario as login_service
from Backend.services.authentication_services import registrar_usuario as registrar_service


@validate_dto(validate_login)
def login_usuario():
    dto = g.dto
    user = login_service(dto['email'], dto['password'])
    token = create_access_token(
        identity=str(user['id']),
        additional_claims={'is_admin': user.get('is_admin', False)}
    )
    return jsonify({'token': token, 'user_id': user['id']}), 200


@validate_dto(validate_register)
def registrar_usuario():
    registrar_service(**g.dto)
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201
