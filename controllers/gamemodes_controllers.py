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
        return ERRORS['UNKNOWN ERROR']
    return jsonify({'gamemodes': gamemodes}), 200


def crear_game_mode(id):
    pass


def reemplazar_game_mode(id):
    pass


def eliminar_game_mode(id):
    pass
