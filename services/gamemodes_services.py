from db import execute


def listar_game_modes():
    gamemodes = execute("SELECT * FROM GameModes")
    if gamemodes is False:
        return None
    return gamemodes


def crear_game_mode(id):
    pass


def reemplazar_game_mode(id):
    pass


def eliminar_game_mode(id):
    pass
