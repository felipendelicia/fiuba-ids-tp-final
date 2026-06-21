from datetime import date, datetime
import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
REVIEWS_PER_PAGE = 2
EQUIP_PER_PAGE = 5
USUARIOS_PER_PAGE = 4
MAPS_PER_PAGE = 10

try:
    from Backend.services.dashboard_services import (
        get_reservas_dia, contar_reservas_dia, get_ingresos_periodo,
        get_frecuencia_horaria, get_calendario_mes, MAX_RESERVAS_POR_DIA
    )
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

    def get_reservas_dia(fecha=None, limit=10, offset=0):
        return []
    def contar_reservas_dia(fecha=None):
        return 0
    def get_ingresos_periodo(fecha):
        return {'dia': 0, 'semana': 0, 'mes': 0, 'año': 0}
    def get_frecuencia_horaria(fecha=None):
        return {'cs': 0, 'so': 0, 'nd': 0, 'od': 0, 'tc': 0, 'qs': 0, 'do': 0, 'dv': 0}
    def get_calendario_mes():
        from datetime import timedelta
        import calendar
        hoy = date.today()
        primer_dia = date(hoy.year, hoy.month, 1)
        inicio_calendario = primer_dia - timedelta(days=primer_dia.weekday())
        dias = []
        for i in range(35):
            d = inicio_calendario + timedelta(days=i)
            dias.append({'num': d.day, 'fecha': d.isoformat(), 'actual': d.month == hoy.month})
        meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
                 'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        return dias, hoy.isoformat(), meses[hoy.month - 1], hoy.year
    MAX_RESERVAS_POR_DIA = 32


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

salas_publicas = []


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





def _api_get_usuario(user_id):
    resp = _api_get(f"/account/{user_id}")
    if resp and resp.status_code == 200:
        cuenta = resp.json().get("Cuenta", {})
        cuenta["user_name"] = cuenta.get("username")
        return cuenta
    return None


def _api_get_maps():
    resp = _api_get("/maps/disponibility", params={"_limit": 100})
    if resp and resp.status_code == 200:
        return resp.json().get("Maps", [])
    return []


def _api_get_gamemodes():
    resp = _api_get("/gamemodes/")
    if resp and resp.status_code == 200:
        return resp.json().get("gamemodes", [])
    return []


def _api_get_equipmentkits():
    resp = _api_get("/equipmentkit/")
    if resp and resp.status_code == 200:
        return resp.json().get("equipmentkits", [])
    return []


def _api_get_equipment_kit(kit_id):
    resp = _api_get(f"/equipmentkit/{kit_id}")
    if resp and resp.status_code == 200:
        return resp.json().get('equipmentkit')
    return None
