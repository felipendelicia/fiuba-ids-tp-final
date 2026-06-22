from flask import request, g, jsonify
from helpers import build_links, send_reservation_mail
from dtos.errors import validate_dto
from dtos.sala_dto import (
    validate_create_sala,
    validate_list_salas,
    validate_update_sala,
    build_sala_response,
)
from dtos.response import build_paginated_response
from services.salas_services import (
    listar_salas as listar_service,
    crear_sala as crear_service,
    actualizar_sala as actualizar_service,
)


@validate_dto(validate_list_salas)
def listar_salas():
    params = g.dto
    salas, total = listar_service(params)
    if total == 0:
        return jsonify({'salas': [], 'total': 0, '_links': {}}), 200
    links = build_links(total, params['offset'], params['limit'])
    return build_paginated_response('salas', salas, total, links, item_builder=build_sala_response)


@validate_dto(validate_create_sala)
def crear_sala():
    user_email = crear_service(g.dto)
    resp = {"message": "Sala creada exitosamente"}
    if g.dto.get("account_id"):
        if user_email:
            send_reservation_mail(user_email, request.get_json())
        resp["message"] = "Sala creada y te has unido exitosamente"
    return jsonify(resp), 201


@validate_dto(validate_update_sala)
def actualizar_sala(id):
    actualizar_service(id, g.dto)
    return jsonify({"message": f"Sala {id} actualizada correctamente"}), 200
