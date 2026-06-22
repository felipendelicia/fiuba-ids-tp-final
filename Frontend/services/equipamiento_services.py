from helpers import _api_get


def _api_get_equipmentkits():
    resp = _api_get("/equipmentkit/")
    if isinstance(resp, Exception):
        return resp
    if resp.status_code != 200:
        return resp
    return resp.json().get("equipmentkits", [])


def _api_get_equipment_kit(kit_id):
    resp = _api_get(f"/equipmentkit/{kit_id}")
    if isinstance(resp, Exception):
        return resp
    if resp.status_code != 200:
        return resp
    return resp.json().get('equipmentkit')
