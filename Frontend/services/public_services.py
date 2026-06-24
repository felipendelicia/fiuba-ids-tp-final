from helpers import _api_get, _api_post


def _api_get_maps():
    resp = _api_get("/maps/disponibility", params={"_limit": 100})
    if isinstance(resp, Exception):
        return resp
    if resp.status_code != 200:
        return resp
    return resp.json().get("Maps", [])


def _api_get_gamemodes():
    resp = _api_get("/gamemodes/")
    if isinstance(resp, Exception):
        return resp
    if resp.status_code != 200:
        return resp
    return resp.json().get("gamemodes", [])


def _api_get_usuario(user_id):
    resp = _api_get(f"/account/{user_id}")
    if isinstance(resp, Exception):
        return resp
    if resp.status_code != 200:
        return resp
    cuenta = resp.json().get("Cuenta", {})
    cuenta["user_name"] = cuenta.get("username")
    return cuenta


def _api_get_contact_messages():
    resp = _api_get("/contacto/")
    if resp and resp.status_code == 200:
        return resp.json()
    return []


def _api_send_contact_message(data):
    resp = _api_post("/contacto/", data=data)
    return resp is not None and resp.status_code == 201


def _api_get_nosotros():
    resp = _api_get("/nosotros/")
    if resp and resp.status_code == 200:
        return resp.json()
    return {'info': None, 'cards': []}
