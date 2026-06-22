from helpers import _api_get


def _api_get_maps():
    resp = _api_get("/maps/disponibility", params={"_limit": 100})
    if isinstance(resp, Exception):
        return resp
    if resp.status_code != 200:
        return resp
    return resp.json().get("Maps", [])
