from helpers import _api_get


def _api_get_usuario(user_id):
    resp = _api_get(f"/account/{user_id}")
    if isinstance(resp, Exception):
        return resp
    if resp.status_code != 200:
        return resp
    cuenta = resp.json().get("Cuenta", {})
    cuenta["user_name"] = cuenta.get("username")
    return cuenta
