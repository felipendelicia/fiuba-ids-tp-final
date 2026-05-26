from db import execute


def listar_game_modes():
    gamemodes = execute("SELECT * FROM GameModes")
    if gamemodes is False:
        return None
    return gamemodes


def crear_game_mode(name, duration, players):
    result = execute(
        "INSERT INTO GameModes (name, duration, players, updated_at) VALUES (%s, %s, %s, CURDATE())",
        (name, duration, players)
    )
    if result is False:
        return None
    return result

def reemplazar_game_mode(id):
    pass


def eliminar_game_mode(id):
    pass
