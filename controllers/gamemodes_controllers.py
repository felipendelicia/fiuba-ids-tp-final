from flask import request, jsonify
from db import execute
from errors import ERRORS
from services.gamemodes_services import (
    listar_game_modes as service_listar_game_modes,
    crear_game_mode as service_crear_game_mode,
    reemplazar_game_mode as service_reemplazar_game_mode,
)

def listar_game_modes():
    gamemodes = service_listar_game_modes()
    if gamemodes is None:
        return ERRORS['UNKNOWN_ERROR']
    return jsonify({'gamemodes': gamemodes}), 200


def crear_game_mode():
    data = request.get_json()
    if data is None:
        return ERRORS['INVALID_FORMAT']("No se encontro JSON validoha")
    if 'name' not in data or 'duration' not in data or 'players' not in data:
        return ERRORS['MISSING_REQUIRED_FIELDS']("Faltan campos obligatorios: name, duration, players")

    name = data['name']
    duration = data['duration']
    players = data['players']

    if name is None or duration is None or players is None:
        return ERRORS['MISSING_REQUIRED_FIELDS']("Faltan campos obligatorios: name, duration, players")

    result = service_crear_game_mode(name, duration, players)
    if result is None:
        return ERRORS['UNKNOWN_ERROR']("Error al crear el game mode")
    return jsonify({'message': 'Game mode creado exitosamente'}), 201


def reemplazar_game_mode(id):
    data = request.get_json()
    if data is None:
        return ERRORS['INVALID_FORMAT']("No se encontro JSON valido")
    if 'name' not in data or 'duration' not in data or 'players' not in data:
        return ERRORS['MISSING_REQUIRED_FIELDS']("Faltan campos obligatorios: name, duration, players")

    name = data['name']
    duration = data['duration']
    players = data['players']

    if name is None or duration is None or players is None:
        return ERRORS['MISSING_REQUIRED_FIELDS']("Faltan campos obligatorios: name, duration, players")

    result = service_reemplazar_game_mode(id, name, duration, players)
    if result is None:
        return ERRORS['NOT_FOUND']("Gamemode no encontrado")
    if result is False:
        return ERRORS['UNKNOWN_ERROR']("Error al reemplazar el game mode")
    return jsonify({'message': 'Game mode reemplazado exitosamente'}), 200


def eliminar_game_mode(id):
    pass
