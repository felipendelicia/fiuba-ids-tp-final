from helpers import _api_get, _api_post, _api_put, _api_delete


def _api_get_services():
    resp = _api_get("/services/")
    if resp and resp.status_code == 200:
        return resp.json().get("services", [])
    return []


def _api_get_service(service_id):
    resp = _api_get(f"/services/{service_id}")
    if resp and resp.status_code == 200:
        return resp.json().get("service")
    return None


def _api_create_service(data):
    resp = _api_post("/services/", data=data)
    return resp is not None and resp.status_code == 201


def _api_update_service(service_id, data):
    resp = _api_put(f"/services/{service_id}", data=data)
    return resp is not None and resp.status_code == 200


def _api_delete_service(service_id):
    resp = _api_delete(f"/services/{service_id}")
    return resp is not None and resp.status_code == 200
