from flask import request, jsonify
from db import execute
from errors import ERRORS
from helpers import build_links


def listar_mapas():
    # Paginación
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
        if limit <= 0 or offset < 0:
            raise ValueError
    except ValueError:
        return ERRORS["INVALID_FORMAT"]("Los parámetros _limit y _offset deben ser enteros positivos.")

    # Contar el total de mapas para los links HATEOAS
    resultado_total = execute("SELECT COUNT(*) as total FROM Maps")
    if resultado_total is False:
        return ERRORS["UNKNOWN_ERROR"]("Error al consultar los mapas.")

    total = resultado_total[0]['total']

    if total == 0:
        return '', 204

    # Traer la página solicitada
    mapas = execute(f"""
        SELECT id, name, image_url, description
        FROM Maps
        LIMIT {limit} OFFSET {offset}
    """)

    if mapas is False:
        return ERRORS["UNKNOWN_ERROR"]("Error al consultar los mapas.")

    links = build_links(total, offset, limit)

    return jsonify({
        "Maps": mapas,
        "_links": links
    }), 200
