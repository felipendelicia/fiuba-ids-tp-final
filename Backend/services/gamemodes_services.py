from Backend.db import execute
from Backend.dtos.errors import abort


def listar_game_modes():
    modos = execute("SELECT * FROM GameModes")

    relaciones = execute("""
        SELECT mgm.gamemode_id, mp.id, mp.name
        FROM MapGameModes mgm
        JOIN Maps mp ON mp.id = mgm.map_id
    """)
    mapas_por_modo = {}
    for r in relaciones:
        mapas_por_modo.setdefault(r['gamemode_id'], []).append({
            'id': r['id'],
            'name': r['name'],
        })

    for m in modos:
        m['maps'] = mapas_por_modo.get(m['id'], [])

    return modos


def crear_game_mode(name, duration, players, description):
    execute(
        f"INSERT INTO GameModes (name, duration, players, description, updated_at) "
        f"VALUES ('{name}', '{duration}', {players}, '{description}', CURDATE())",
    )


def reemplazar_game_mode(id, name, duration, players, description):
    gamemode = execute(f"SELECT id FROM GameModes WHERE id = {id}")
    if not gamemode:
        abort(404, 'Gamemode no encontrado')
    execute(
        f"UPDATE GameModes SET name = '{name}', duration = '{duration}', players = {players}, description = '{description}', updated_at = CURDATE() WHERE id = {id}",
    )


def eliminar_game_mode(id):
    gamemode = execute(f"SELECT id FROM GameModes WHERE id = {id}")
    if not gamemode:
        abort(404, 'Gamemode no encontrado')
    execute(f"DELETE FROM MapGameModes WHERE gamemode_id = {id}")
    execute(f"DELETE FROM GameModes WHERE id = {id}")


def reemplazar_mapas_de_modo(gamemode_id, map_ids):
    gamemode = execute(f"SELECT id FROM GameModes WHERE id = {gamemode_id}")
    if not gamemode:
        abort(404, 'Gamemode no encontrado')
    execute(f"DELETE FROM MapGameModes WHERE gamemode_id = {gamemode_id}")
    for mid in map_ids:
        execute(f"INSERT INTO MapGameModes (gamemode_id, map_id) VALUES ({gamemode_id}, {int(mid)})")
