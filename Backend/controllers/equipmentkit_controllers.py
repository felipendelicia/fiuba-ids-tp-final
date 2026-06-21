from flask import g, jsonify
from Backend.helpers import build_links
from Backend.dtos.errors import validate_dto
from Backend.dtos.equipment_dto import (
    validate_list_equipment,
    validate_create_equipment,
    build_equipment_response,
)
from Backend.dtos.response import build_paginated_response, build_created_response, build_updated_response
from Backend.services.equipmentkit_services import (
    listar_kit_equipamientos as service_listar,
    obtener_kit_equipamiento as service_obtener,
    crear_kit_equipamiento as service_crear,
    reemplazar_kit_equipamiento as service_reemplazar,
    eliminar_kit_equipamiento as service_eliminar,
)


@validate_dto(validate_list_equipment)
def listar_kit_equipamientos():
    params = g.dto
    kits, total = service_listar(params['offset'], params['limit'])
    links = build_links(total, params['offset'], params['limit'])
    return build_paginated_response('equipmentkits', kits, total, links, item_builder=build_equipment_response)


def obtener_kit_equipamiento(id):
    kit = service_obtener(id)
    return jsonify({'equipmentkit': build_equipment_response(kit)}), 200


@validate_dto(validate_create_equipment)
def crear_kit_equipamiento():
    service_crear(**g.dto)
    return build_created_response('Kit de equipamiento creado exitosamente')


@validate_dto(validate_create_equipment)
def reemplazar_kit_equipamiento(id):
    service_reemplazar(id, **g.dto)
    return build_updated_response('Kit de equipamiento reemplazado exitosamente')


def eliminar_kit_equipamiento(id):
    service_eliminar(id)
    return jsonify({'message': 'Kit de equipamiento eliminado exitosamente'}), 200
