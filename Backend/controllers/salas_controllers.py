from flask import request, g, jsonify
from helpers import build_links, send_reservation_mail, send_cancelation_mail
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
    dto = g.dto
    user_email = crear_service(dto)

    if user_email:
        mail_body = {
            **dto,
            'is_public': dto.get('is_public', True),
        }
        if not send_reservation_mail(user_email, mail_body):
            print("Advertencia: mail no pudo enviarse al crear la sala")

    return jsonify({"message": "Sala creada exitosamente"}), 201


@validate_dto(validate_update_sala)
def actualizar_sala(id):
    actualizar_service(id, g.dto)

    if g.dto.get('canceled'):
        sala = execute(f"SELECT * FROM Salas WHERE id = {id}")
        if sala:
            s = sala[0]
            reservations = execute(f"""SELECT r.*, a.email
                                       FROM Reservations r
                                       JOIN Accounts a ON r.account_id = a.id
                                       WHERE r.sala_id = {id} AND r.canceled = TRUE""")
            for res in reservations:
                mail_body = {
                    'account_id': res['account_id'],
                    'map_id': s['map_id'],
                    'reservation_date': str(s.get('reservation_date', '')),
                    'start_time': str(s.get('start_time', '')),
                    'end_time': str(s.get('end_time', '')),
                    'cancelation_reason': s.get('cancelation_reason') or 'Sala cancelada por el administrador',
                }
                if not send_cancelation_mail(res['email'], mail_body):
                    print(f"Advertencia: mail de cancelación no pudo enviarse a {res['email']}")

    return jsonify({"message": f"Sala {id} actualizada correctamente"}), 200
