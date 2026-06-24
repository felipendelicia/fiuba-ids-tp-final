from flask import request, g, jsonify
from helpers import build_links
from dtos.errors import validate_dto, abort
from dtos.map_dto import validate_list_maps, build_map_response
from services.maps_services import listar_mapas as listar_mapas_service


@validate_dto(validate_list_maps)
def listar_mapas():
    params = g.dto
    mapas, total = listar_mapas_service(params['limit'], params['offset'])

    if total == 0:
        return '', 204

    links = build_links(total, params['offset'], params['limit'])
    return jsonify({
        'Maps': [build_map_response(m) for m in mapas],
        '_links': links,
    }), 200
