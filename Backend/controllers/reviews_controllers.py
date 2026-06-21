from flask import g
from flask_jwt_extended import jwt_required
from Backend.helpers import build_links
from Backend.dtos.errors import validate_dto, admin_required, abort
from Backend.dtos.review_dto import (
    validate_list_reviews,
    validate_create_review,
    validate_update_review,
    build_review_response,
)
from Backend.dtos.response import build_paginated_response, build_created_response, build_updated_response
from Backend.services.reviews_services import (
    listar_reviews as listar_reviews_service,
    crear_map_review as crear_review_service,
    actualizar_review as actualizar_review_service,
)


@jwt_required()
@validate_dto(validate_list_reviews)
def listar_reviews():
    params = g.dto
    reviews, total = listar_reviews_service(params['offset'], params['limit'], params['approved'])
    links = build_links(total, params['offset'], params['limit'])
    return build_paginated_response('reviews', reviews, total, links, item_builder=build_review_response)


@jwt_required()
@validate_dto(validate_create_review)
def crear_map_review():
    crear_review_service(**g.dto)
    return build_created_response('Reseña creada exitosamente')


@jwt_required()
@admin_required
@validate_dto(validate_update_review)
def actualizar_review(id):
    actualizar_review_service(id, g.dto['approved'])
    return build_updated_response('Reseña actualizada exitosamente')
