from flask import g, jsonify
from helpers import build_links
from dtos.errors import validate_dto
from dtos.account_dto import (
    validate_list_accounts,
    validate_update_user,
    validate_toggle_status,
    validate_update_gender,
    validate_update_password,
    build_user_response,
)
from dtos.response import build_paginated_response
from services.account_services import (
    listar_usuarios as listar_usuarios_service,
    obtener_cuenta as obtener_cuenta_service,
    actualizar_usuario as actualizar_usuario_service,
    actualizar_estado_usuario as actualizar_estado_usuario_service,
    actualizar_genero_usuario as actualizar_genero_usuario_service,
    actualizar_password_usuario as actualizar_password_usuario_service,
)


@validate_dto(validate_list_accounts)
def listar_usuarios():
    params = g.dto
    usuarios, total = listar_usuarios_service(params['limit'], params['offset'])
    links = build_links(total, params['offset'], params['limit'])
    return build_paginated_response('Listado de Usuarios', usuarios, total, links, item_builder=build_user_response)


def obtener_cuenta(id):
    usuario = obtener_cuenta_service(id)
    return jsonify({'Cuenta': build_user_response(usuario)}), 200


def listar_reservas(id):
    pass


@validate_dto(validate_update_user)
def actualizar_usuario(id):
    actualizar_usuario_service(id, **g.dto)
    return '', 204


@validate_dto(validate_toggle_status)
def actualizar_estado_usuario(id):
    actualizar_estado_usuario_service(id, g.dto['is_active'])
    return '', 204


@validate_dto(validate_update_gender)
def actualizar_genero_usuario(id):
    actualizar_genero_usuario_service(id, g.dto['gender'])
    return '', 204


@validate_dto(validate_update_password)
def actualizar_password_usuario(id):
    actualizar_password_usuario_service(id, g.dto['password'])
    return '', 204
