from flask import request, jsonify
from db import execute
from errors import ERRORS
from helpers import build_links
from services.account_services import listar_usuarios as listar_usuarios_service
from services.account_services import obtener_cuenta as obtener_cuenta_service
from services.account_services import actualizar_usuario as actualizar_usuario_service
from services.account_services import actualizar_estado_usuario as actualizar_estado_usuario_service
from services.account_services import actualizar_genero_usuario as actualizar_genero_usuario_service
from services.account_services import actualizar_password_usuario as actualizar_password_usuario_service

def listar_usuarios():
    usuarios = listar_usuarios_service()
    if not usuarios:
        return ERRORS['NOT_FOUND']('No se encontraron usuarios')
    return jsonify({'Listado de Usuarios': usuarios}), 200

def obtener_cuenta(id):
    usuario_id = obtener_cuenta_service(id)
    if not usuario_id:
        return ERRORS['NOT_FOUND']('Usuario con el id no encontrado')
    return jsonify({'Cuenta': usuario_id}), 200

def actualizar_usuario(id):
    data = request.get_json()
    if ('username' not in data) or ('email' not in data) or ('password' not in data) or ('phone' not in data) or ('elo' not in data) or ('is_active' not in data):
        return ERRORS['MISSING_REQUIRED_FIELDS']('Los campos son: username, email, password, phone, elo, is_active')
    username = data['username']
    email = data['email']
    password = data['password']
    phone = data['phone']
    elo = data['elo']
    is_active = data['is_active']
    estado = actualizar_usuario_service(id, username, email, password, phone, elo, is_active)
    if estado is None:
        return ERRORS['NOT_FOUND']("Usuario con el id no encontrado")
    if estado == False:
        return ERRORS['UNKNOWN_ERROR']("Error al actualizar usuario")
    return '', 204

def listar_reservas(id):
    pass

def actualizar_estado_usuario(id):
    data = request.get_json()
    if ('is_active' not in data):
        return ERRORS['MISSING_REQUIRED_FIELDS']('EL campo es: is_active')
    is_active = data['is_active']
    estado = actualizar_estado_usuario_service(id, is_active)
    if estado is None:
        return ERRORS['NOT_FOUND']("Usuario con el id no encontrado")
    if estado == False:
        return ERRORS['UNKNOWN_ERROR']("Error al actualizar usuario")
    return '', 204

def actualizar_genero_usuario(id):
    data = request.get_json()
    if ('gender' not in data):
        return ERRORS['MISSING_REQUIRED_FIELDS']('El campo es: gender')
    gender = data['gender']
    estado = actualizar_genero_usuario_service(id, gender)
    if estado is None:
        return ERRORS['NOT_FOUND']("Usuario con el id no encontrado")
    if estado == False:
        return ERRORS['UNKNOWN_ERROR']("Error al actualizar usuario")
    return '', 204

def actualizar_password_usuario(id):
    data = request.get_json()
    if ('password' not in data):
        return ERRORS['MISSING_REQUIRED_FIELDS']('El campo es: password')
    password = data['password']
    estado = actualizar_password_usuario_service(id, password)
    if estado is None:
        return ERRORS['NOT_FOUND']("Usuario con el id no encontrado")
    if estado == False:
        return ERRORS['UNKNOWN_ERROR']("Error al actualizar usuario")
    return '', 204