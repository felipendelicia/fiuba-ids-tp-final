from datetime import date, timedelta
import calendar as calmod
import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def _fetch_dashboard_data(fecha):
    try:
        resp = requests.get(
            f"{BACKEND_URL}/dashboard/data/",
            params={"date": fecha, "_limit": 100, "_offset": 0},
            timeout=5,
        )
        if resp.status_code == 200:
            return resp.json()
    except requests.RequestException:
        pass
    return {"reservas": [], "frecuencia": {}, "ingresos": {}, "total": 0, "total_capacidad": 0}


def get_reservas_dia(fecha=None, limit=100, offset=0):
    if not fecha:
        fecha = date.today().isoformat()
    data = _fetch_dashboard_data(fecha)
    return data.get("reservas", [])


def contar_reservas_dia(fecha=None):
    if not fecha:
        fecha = date.today().isoformat()
    data = _fetch_dashboard_data(fecha)
    return data.get("total", 0)


def contar_capacidad_dia(fecha=None):
    if not fecha:
        fecha = date.today().isoformat()
    data = _fetch_dashboard_data(fecha)
    return data.get("total_capacidad", 0)


def get_ingresos_periodo(fecha):
    if not fecha:
        fecha = date.today().isoformat()
    data = _fetch_dashboard_data(fecha)
    ingresos = data.get("ingresos", {})
    return {
        "dia": int(ingresos.get("dia", 0) or 0),
        "semana": int(ingresos.get("semana", 0) or 0),
        "mes": int(ingresos.get("mes", 0) or 0),
        "año": int(ingresos.get("año", 0) or 0),
    }


def get_frecuencia_horaria(fecha=None):
    if not fecha:
        fecha = date.today().isoformat()
    data = _fetch_dashboard_data(fecha)
    raw = data.get("frecuencia", {})
    slots = ["cs", "so", "nd", "od", "tc", "qs", "do", "dv"]
    return {s: int(raw.get(s, 0) or 0) for s in slots}


def get_calendario_mes():
    hoy = date.today()
    primer_dia = date(hoy.year, hoy.month, 1)
    inicio_calendario = primer_dia - timedelta(days=primer_dia.weekday())
    dias = []
    for i in range(35):
        d = inicio_calendario + timedelta(days=i)
        dias.append({"num": d.day, "fecha": d.isoformat(), "actual": d.month == hoy.month})
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    ]
    return dias, hoy.isoformat(), meses[hoy.month - 1], hoy.year
