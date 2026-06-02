from flask import jsonify, g
from helpers import build_links
from dtos.errors import validate_dto
from dtos.dashboard_dto import validate_disponibility
from services.dashboard_services import listar_periodo_reservas


@validate_dto(validate_disponibility)
def listar_periodo_reservas():
    params = g.dto
    reservas, total = listar_periodo_reservas(params['limit'], params['offset'])

    if total == 0:
        return '', 204

    items = [{
        'id_reserva': r['id'],
        'user_name': r['user_name'],
        'dni_usuario': r['dni_usuario'],
        'price': r['price'],
        'start_time': str(r['start_time']),
        'end_time': str(r['end_time']),
    } for r in reservas]

    links = build_links(total, params['offset'], params['limit'])

    return jsonify({
        'Dashboard': items,
        '_links': links,
    }), 200
