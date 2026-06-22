from helpers import _api_get


def _api_get_gamemodes():
    resp = _api_get("/gamemodes/")
    if isinstance(resp, Exception):
        return resp
    if resp.status_code != 200:
        return resp
    return resp.json().get("gamemodes", [])
