from flask import request, jsonify
from db import execute
from errors import ERRORS
from helpers import build_links
from services.account_services import listar_usuarios as listar_usuarios_service
from services.account_services import obtener_cuenta as obtener_cuenta_service


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
    pass

def listar_reservas(id):
    #Paginación
    pass

def actualizar_estado_usuario(id):
    pass

def actualizar_genero_usuario(id):
    pass

def actualizar_password_usuario(id):
    pass
