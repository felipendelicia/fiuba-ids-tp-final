from flask import g, jsonify
from dtos.errors import validate_dto
from dtos.gamemode_dto import (
    validate_create_gamemode,
    validate_map_ids,
    build_gamemode_response,
)
from dtos.response import build_created_response, build_updated_response
from services.gamemodes_services import (
    listar_game_modes as service_listar_game_modes,
    crear_game_mode as service_crear_game_mode,
    reemplazar_game_mode as service_reemplazar_game_mode,
    eliminar_game_mode as service_eliminar_game_mode,
    reemplazar_mapas_de_modo as service_reemplazar_mapas_de_modo,
)

def listar_game_modes():
    gamemodes = service_listar_game_modes()
    return jsonify({'gamemodes': [build_gamemode_response(g) for g in gamemodes]}), 200


@validate_dto(validate_create_gamemode)
def crear_game_mode():
    service_crear_game_mode(**g.dto)
    return build_created_response('Gamemode creado exitosamente')


@validate_dto(validate_create_gamemode)
def reemplazar_game_mode(id):
    service_reemplazar_game_mode(id, **g.dto)
    return build_updated_response('Gamemode reemplazado exitosamente')


def eliminar_game_mode(id):
    service_eliminar_game_mode(id)
    return jsonify({'message': 'Gamemode eliminado exitosamente'}), 200


@validate_dto(validate_map_ids)
def reemplazar_mapas_de_modo(id):
    service_reemplazar_mapas_de_modo(id, **g.dto)
    return build_updated_response('Mapas actualizados exitosamente')
