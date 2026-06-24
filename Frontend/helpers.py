import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
REVIEWS_PER_PAGE = 2
EQUIP_PER_PAGE = 5
USUARIOS_PER_PAGE = 4


slot_map = {
    'cs': ('05:00:00', '07:00:00'),
    'so': ('07:00:00', '09:00:00'),
    'nd': ('09:00:00', '11:00:00'),
    'od': ('11:00:00', '13:00:00'),
    'tc': ('13:00:00', '15:00:00'),
    'qs': ('15:00:00', '17:00:00'),
    'do': ('17:00:00', '19:00:00'),
    'dv': ('19:00:00', '21:00:00'),
}


def _api_request(method, endpoint, data=None, token=None, params=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        return requests.request(
            method, f"{BACKEND_URL}{endpoint}",
            json=data, params=params, headers=headers, timeout=5
        )
    except requests.RequestException:
        return None


def _api_get(endpoint, params=None, token=None):
    return _api_request("GET", endpoint, params=params, token=token)


def _api_post(endpoint, data=None, token=None):
    return _api_request("POST", endpoint, data=data, token=token)


def _api_put(endpoint, data=None, token=None):
    return _api_request("PUT", endpoint, data=data, token=token)


def _api_patch(endpoint, data=None, token=None):
    return _api_request("PATCH", endpoint, data=data, token=token)


def _api_delete(endpoint, token=None):
    return _api_request("DELETE", endpoint, token=token)

