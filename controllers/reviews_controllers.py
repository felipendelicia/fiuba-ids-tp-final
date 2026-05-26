from flask import request, jsonify
from flask_jwt_extended import jwt_required
from errors import ERRORS
from helpers import build_links
from services.reviews_services import (
    listar_reviews as listar_reviews_service,
    crear_map_review as crear_review_service,
    actualizar_review as actualizar_review_service,
)


def listar_reviews():
    try:
        offset = int(request.args.get('_offset', 0))
        limit = int(request.args.get('_limit', 10))
    except ValueError:
        return ERRORS['INVALID_FORMAT']('_offset y _limit deben ser enteros')

    reviews, total = listar_reviews_service(offset, limit)
    if reviews is None:
        return ERRORS['UNKNOWN_ERROR']('Error al obtener reseñas')

    links = build_links(total, offset, limit)
    return jsonify({'reviews': reviews, 'total': total, '_links': links}), 200


@jwt_required()
def crear_map_review():
    data = request.get_json()
    stars = data.get('stars')
    map_id = data.get('map_id')
    body_review = data.get('body_review', '')

    if stars is None or map_id is None:
        return ERRORS['MISSING_REQUIRED_FIELDS']('stars y map_id son requeridos')

    if not isinstance(stars, int) or not (1 <= stars <= 5):
        return ERRORS['INVALID_FORMAT']('stars debe ser un entero entre 1 y 5')

    success, error = crear_review_service(stars, body_review, map_id)
    if error == 'not_found':
        return ERRORS['NOT_FOUND']('Mapa no encontrado')
    if not success:
        return ERRORS['UNKNOWN_ERROR']('Error al crear la reseña')

    return jsonify({'message': 'Reseña creada exitosamente'}), 201


@jwt_required()
def actualizar_review(id):
    data = request.get_json()
    approved = data.get('approved')

    if approved is None:
        return ERRORS['MISSING_REQUIRED_FIELDS']('approved es requerido')

    if not isinstance(approved, bool):
        return ERRORS['INVALID_FORMAT']('approved debe ser un booleano')

    success, error = actualizar_review_service(id, approved)
    if error == 'not_found':
        return ERRORS['NOT_FOUND']('Reseña no encontrada')
    if not success:
        return ERRORS['UNKNOWN_ERROR']('Error al actualizar la reseña')

    return jsonify({'message': 'Reseña actualizada exitosamente'}), 200
