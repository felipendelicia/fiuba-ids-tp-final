from helpers import _api_get, _api_post, _api_put, _api_delete


def _api_get_competitivo_events():
    resp = _api_get("/competitivo/")
    if resp and resp.status_code == 200:
        return resp.json().get("events", [])
    return []


def _api_create_competitivo_event(data):
    resp = _api_post("/competitivo/", data=data)
    return resp is not None and resp.status_code == 201


def _api_update_competitivo_event(id, data):
    resp = _api_put(f"/competitivo/{id}", data=data)
    return resp is not None and resp.status_code == 200


def _api_delete_competitivo_event(id):
    resp = _api_delete(f"/competitivo/{id}")
    return resp is not None and resp.status_code == 200
