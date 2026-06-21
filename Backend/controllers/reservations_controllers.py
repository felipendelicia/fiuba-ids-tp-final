from flask import request, g, jsonify
from helpers import build_links, send_reservation_mail
from dtos.errors import validate_dto
from dtos.reservation_dto import (
    validate_list_reservations,
    validate_list_user_reservations,
    validate_create_reservation,
    validate_create_public_reservation,
    validate_update_reservation,
    build_reservation_response,
)
from dtos.response import build_paginated_response
from services.reservations_services import (
    listar_reservas as listar_service,
    listar_reservas_usuario as listar_reservas_usuario_service,
    crear_reserva as crear_service,
    actualizar_reserva as actualizar_service,
)


@validate_dto(validate_list_reservations)
def listar_reservas():
    params = g.dto
    reservas, total = listar_service(params)
    links = build_links(total, params['offset'], params['limit'])
    return build_paginated_response('reservas', reservas, total, links, item_builder=build_reservation_response)


@validate_dto(validate_list_user_reservations)
def listar_reservas_usuario(id):
    reservas, total = listar_reservas_usuario_service(g.dto, id)
    links = build_links(total, g.dto['offset'], g.dto['limit'])
    return build_paginated_response('reservas', reservas, total, links, item_builder=build_reservation_response)


@validate_dto(validate_create_reservation)
def crear_reserva(id):
    dto = {**g.dto, 'game_mode_id': id, 'is_public': False}
    user_email = crear_service(dto)
    if not send_reservation_mail(user_email, g.dto):
        print("Advertencia: mail no pudo enviarse")
    return jsonify({"message": "Reserva creada exitosamente"}), 200


@validate_dto(validate_update_reservation)
def actualizar_reserva(id):
    actualizar_service(id, g.dto)
    return jsonify({"message": f"Reserva {id} actualizada correctamente"}), 200


@validate_dto(validate_create_public_reservation)
def crear_public_reservation(id):
    dto = {**g.dto, 'game_mode_id': id, 'is_public': True}
    user_email = crear_service(dto)
    if not send_reservation_mail(user_email, g.dto):
        print("Advertencia: mail no pudo enviarse")
    return jsonify({"message": "Reserva creada exitosamente"}), 200
