from flask import request, g, jsonify
from helpers import build_links, send_reservation_mail
from db import execute
from dtos.errors import validate_dto
from dtos.reservation_dto import (
    validate_join_sala,
    validate_list_reservations,
    validate_update_reservation,
    build_reservation_response,
)
from dtos.response import build_paginated_response
from services.reservations_services import (
    listar_reservas as listar_service,
    crear_reserva as crear_service,
    actualizar_reserva as actualizar_service,
)


@validate_dto(validate_list_reservations)
def listar_reservas():
    params = g.dto
    reservas, total = listar_service(params)
    links = build_links(total, params['offset'], params['limit'])
    return build_paginated_response('reservas', reservas, total, links, item_builder=build_reservation_response)


@validate_dto(validate_join_sala)
def join_sala(sala_id):
    dto = g.dto
    user_email = crear_service(sala_id, dto)

    sala_rows = execute(f"SELECT * FROM Salas WHERE id = {sala_id}")
    sala = sala_rows[0] if sala_rows else {}
    mail_body = {
        **dto,
        'sala_id': sala_id,
        'map_id': sala.get('map_id'),
        'reservation_date': str(sala.get('reservation_date', '')),
        'is_public': sala.get('is_public'),
        'start_time': str(sala.get('start_time', '')),
        'end_time': str(sala.get('end_time', '')),
    }

    if not send_reservation_mail(user_email, mail_body):
        print("Advertencia: mail no pudo enviarse")
    return jsonify({"message": "Te uniste a la sala exitosamente"}), 200


@validate_dto(validate_update_reservation)
def actualizar_reserva(id):
    actualizar_service(id, g.dto)
    return jsonify({"message": f"Reserva {id} actualizada correctamente"}), 200
