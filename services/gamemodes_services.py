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

def reemplazar_game_mode(id, name, duration, players):
    gamemode = execute(f"SELECT * FROM GameModes WHERE id = {id}")
    if gamemode is False or not gamemode:
        return None
    result = execute(
        f"UPDATE GameModes SET name = '{name}', duration = '{duration}', players = {players}, updated_at = CURDATE() WHERE id = {id}",
    )
    if result is False:
        return None
    return result


def eliminar_game_mode(id):
    pass
