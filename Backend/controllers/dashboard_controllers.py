from datetime import date
from flask import jsonify, g, request
from helpers import build_links
from dtos.errors import validate_dto
from dtos.dashboard_dto import validate_disponibility
from services.dashboard_services import listar_periodo_reservas as service_listar_reservas, get_dashboard_data


@validate_dto(validate_disponibility)
def listar_periodo_reservas():
    params = g.dto
    fecha = request.args.get('date')
    reservas, total = service_listar_reservas(params['limit'], params['offset'], fecha)

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


def api_dashboard_data():
    fecha = request.args.get('date', date.today().isoformat())
    limit = int(request.args.get('_limit', 100))
    offset = int(request.args.get('_offset', 0))

    reservas, frecuencia, ingresos, total, total_capacidad = get_dashboard_data(fecha, limit, offset)

    items = []
    for r in reservas:
        items.append({
            'id_reserva': r['id'],
            'user_name': r['user_name'],
            'dni_usuario': r['dni_usuario'],
            'price': r['price'],
            'start_time': str(r['start_time']),
            'end_time': str(r['end_time']),
            'map_name': r.get('map_name', ''),
        })

    frecuencia = {k: int(v) for k, v in frecuencia.items()}

    return jsonify({
        'reservas': items,
        'frecuencia': frecuencia,
        'ingresos': ingresos,
        'total': total,
        'total_capacidad': total_capacidad,
    })
