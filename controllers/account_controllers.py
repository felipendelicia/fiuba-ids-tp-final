from flask import request, jsonify
from db import execute
from errors import ERRORS
from helpers import build_links
from services.account_services import listar_usuarios as listar_usuarios_service
from services.account_services import obtener_cuenta as obtener_cuenta_service


def listar_usuarios():
    #Paginación
    usuarios = listar_usuarios_service()

    #Manejo de errores
    if not usuarios:
        return ERRORS['NOT_FOUND']('No se encontro usuarios')

    return jsonify({'Listado de Usuarios': usuarios})

def obtener_cuenta(id):

    usuario_id = obtener_cuenta_service(id)
    #Manejo de erores;
    
    # if type(id) != int:
    #     return ERRORS['INVALID_FORMAT']('El id debe ser un entero')
        
    if not usuario_id:
        return ERRORS['NOT_FOUND']('Usuario no encontrado')
    
    
    #    return ERRORS['UNKNOWN_ERROR']('comunicate con nosotros'), 500
    
    return jsonify({'id': usuario_id}), 200

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
