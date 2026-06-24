from helpers import _api_get

def _api_get_equipmentkits(category=None):
    params = {"_limit": 100}
    if category:
        params["category"] = category
    resp = _api_get("/equipmentkit/", params=params)
    if resp and resp.status_code == 200:
        return resp.json().get("equipmentkits", [])
    return []


def _api_get_equipment_categories():
    resp = _api_get("/equipmentkit/categories")
    if resp and resp.status_code == 200:
        return resp.json().get("categories", [])
    return []


def _api_get_equipment_kit(kit_id):
    resp = _api_get(f"/equipmentkit/{kit_id}")
    if resp and resp.status_code == 200:
        return resp.json().get('equipmentkit')
    return None