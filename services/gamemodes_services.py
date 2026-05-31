from db import execute
from dtos.errors import abort


def listar_game_modes():
    return execute("SELECT * FROM GameModes")


def crear_game_mode(name, duration, players):
    execute(
        f"INSERT INTO GameModes (name, duration, players, updated_at) "
        f"VALUES ('{name}', '{duration}', {players}, CURDATE())",
    )


def reemplazar_game_mode(id, name, duration, players):
    gamemode = execute(f"SELECT id FROM GameModes WHERE id = {id}")
    if not gamemode:
        abort(404, 'Gamemode no encontrado')
    execute(
        f"UPDATE GameModes SET name = '{name}', duration = '{duration}', players = {players}, updated_at = CURDATE() WHERE id = {id}",
    )


def eliminar_game_mode(id):
    gamemode = execute(f"SELECT id FROM GameModes WHERE id = {id}")
    if not gamemode:
        abort(404, 'Gamemode no encontrado')
    execute(f"DELETE FROM GameModes WHERE id = {id}")
