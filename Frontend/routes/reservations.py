from datetime import date, timedelta
from flask import flash, render_template, request, redirect, url_for, session, jsonify
from helpers import (
    slot_map as slot_map_dict,
    _api_get, _api_post, _api_patch
)
from services.public_services import _api_get_maps, _api_get_gamemodes
from services.dashboard_services import get_frecuencia_horaria


def register(app):

    @app.route("/perfil/reservasadmin/crearsala", methods=['POST'])
    def admin_crearsala():
        usuario = session.get('usuario')
        if not usuario:
            flash("Debes iniciar sesion para realizar una reserva.", "warning")
            return redirect(url_for('login_sesion'))

        game_mode_id = request.form.get("modalidad")
        turno = request.form.get("turno")
        start_time, end_time = slot_map_dict.get(turno, (None, None))
        if not start_time:
            flash("Selecciona un turno valido.", "warning")
            return redirect(url_for('lobby_user'))

        modalidades = _api_get_gamemodes()
        modalidad_max_players = 4
        if not isinstance(modalidades, Exception):
            for m in modalidades:
                if str(m["id"]) == game_mode_id:
                    modalidad_max_players = m.get("players", 4)
                    break

        payload = {
            "game_mode_id": int(game_mode_id),
            "map_id": int(request.form.get("map_id")),
            "price": int(request.form.get("price")),
            "reservation_date": request.form.get("reservation_date"),
            "start_time": start_time,
            "end_time": end_time,
            "max_players": modalidad_max_players,
            "admin_account_id": int(usuario["id"]),
            "is_public": True,
        }
        resp = _api_post("/salas/", data=payload, token=usuario.get('token'))
        if isinstance(resp, Exception):
            flash(f"Error de conexion: {resp}", "warning")
        elif resp.status_code == 201:
            flash("Sala creada exitosamente.", "success")
        elif resp.status_code == 401:
            flash("Tu sesion expiro. Volve a iniciar sesion.", "warning")
            return redirect(url_for('login_sesion'))
        else:
            try:
                body = resp.json()
                msg = body.get("message")
                if not msg:
                    errors = body.get("errors", [])
                    if errors:
                        msg = errors[0].get("message", "No se pudo crear la sala.")
                    else:
                        msg = "No se pudo crear la sala."
            except Exception:
                msg = "No se pudo crear la sala."
            flash(msg, "warning")
        return redirect(url_for('lobby_user'))

    @app.route("/lobby/unirse-publica", methods=["POST"])
    def unirse_sala_publica():
        usuario = session.get('usuario')
        if not usuario:
            flash("Debes iniciar sesion.", "warning")
            return redirect(url_for('login_sesion'))

        sala_id = request.form.get("sala_id")
        equipment_kit_id = request.form.get("equipment_kit_id")
        total_price = request.form.get("total_price", "0")

        if not sala_id:
            flash("Faltan datos para unirse a la sala.", "warning")
            return redirect(url_for('lobby_user'))

        payload = {
            "account_id": int(usuario["id"]),
            "equipment_kit_id": int(equipment_kit_id) if equipment_kit_id else 1,
            "price": int(total_price),
        }
        resp = _api_post(f"/reservations/register/{sala_id}", data=payload, token=usuario.get('token'))
        if isinstance(resp, Exception):
            flash(f"Error de conexion: {resp}", "warning")
        elif resp.status_code == 200:
            flash("Te uniste a la sala exitosamente.", "success")
        else:
            try:
                body = resp.json()
                msg = body.get("message")
                if not msg:
                    errors = body.get("errors", [])
                    if errors:
                        msg = errors[0].get("message", "No se pudo unir a la sala.")
                    else:
                        msg = "No se pudo unir a la sala."
            except Exception:
                msg = "No se pudo unir a la sala."
            flash(msg, "warning")
        return redirect(url_for('lobby_user'))

    @app.route("/lobby/reserva/<int:reservation_id>/cancelar", methods=["POST"])
    def cancelar_reserva(reservation_id):
        usuario = session.get('usuario')
        if not usuario:
            flash("Debes iniciar sesion.", "warning")
            return redirect(url_for('login_sesion'))

        resp = _api_patch(f"/reservations/{reservation_id}", data={"canceled": True, "account_id": usuario["id"]}, token=usuario.get('token'))
        if isinstance(resp, Exception):
            flash(f"Error de conexion: {resp}", "warning")
        elif resp.status_code == 200:
            flash("Reserva cancelada exitosamente.", "success")
        else:
            try:
                body = resp.json()
                msg = body.get("message")
                if not msg:
                    errors = body.get("errors", [])
                    if errors:
                        msg = errors[0].get("message", "No se pudo cancelar la reserva.")
                    else:
                        msg = "No se pudo cancelar la reserva."
            except Exception:
                msg = "No se pudo cancelar la reserva."
            flash(msg, "warning")
        return redirect(url_for('lobby_user'))

    @app.route("/lobby/sala/<int:sala_id>/cancelar", methods=["POST"])
    def cancelar_sala(sala_id):
        usuario = session.get('usuario')
        if not usuario:
            flash("Debes iniciar sesion.", "warning")
            return redirect(url_for('login_sesion'))

        resp = _api_patch(f"/salas/{sala_id}", data={"canceled": True, "admin_account_id": usuario["id"]}, token=usuario.get('token'))
        if isinstance(resp, Exception):
            flash(f"Error de conexion: {resp}", "warning")
        elif resp.status_code == 200:
            flash("Sala cancelada exitosamente. Todas las reservas asociadas fueron canceladas.", "success")
        else:
            try:
                body = resp.json()
                msg = body.get("message")
                if not msg:
                    errors = body.get("errors", [])
                    if errors:
                        msg = errors[0].get("message", "No se pudo cancelar la sala.")
                    else:
                        msg = "No se pudo cancelar la sala."
            except Exception:
                msg = "No se pudo cancelar la sala."
            flash(msg, "warning")
        return redirect(url_for('lobby_user'))

    @app.route("/lobby_user")
    def lobby_user():
        usuario = session.get('usuario')
        if not usuario:
            flash("Debes iniciar sesion para acceder a las salas publicas.", "warning")
            return redirect(url_for('login_sesion'))

        resp = _api_get("/salas/", params={"is_public": "1", "_limit": 100}, token=usuario.get('token'))
        if resp is None:
            flash("Error de conexion al cargar salas.", "warning")
            return render_template('lobby_user.html', salas=[], usuario=usuario)
        salas_data = resp.json().get("salas", []) if resp.status_code == 200 else []

        modalidades = _api_get_gamemodes()
        if isinstance(modalidades, Exception):
            modalidades = []
        modalidad_map = {m["id"]: m["name"] for m in modalidades}
        modalidades_admin = modalidades if usuario.get("is_admin") else []

        mapas = _api_get_maps()
        if isinstance(mapas, Exception):
            mapas = []
        mapa_map = {m["id"]: m["name"] for m in mapas}
        mapas_admin = mapas if usuario.get("is_admin") else []

        reservas_resp = _api_get("/reservations/", params={"_limit": 1000}, token=usuario.get('token'))
        user_reservas = []
        if reservas_resp and reservas_resp.status_code == 200:
            all_reservas = reservas_resp.json().get("reservas", [])
            user_reservas = [r for r in all_reservas if r.get("account_id") == usuario["id"] and not r.get("canceled")]

        user_sala_ids = {r["sala_id"] for r in user_reservas}

        salas = []
        reservas_json = []
        for s in salas_data:
            if s.get("canceled"):
                continue
            current = s.get("current_players", 0)
            maximos = s.get("max_players", 4)
            unido = s["id"] in user_sala_ids
            user_reservation_id = None
            user_reservation_price = None
            for r in user_reservas:
                if r["sala_id"] == s["id"]:
                    user_reservation_id = r["id"]
                    user_reservation_price = r.get("price")
                    break
            es_admin_sala = usuario.get("is_admin")
            sala_precio = user_reservation_price if user_reservation_price else s.get("price", 0)
            salas.append({
                "id": s["id"],
                "user_reservation_id": user_reservation_id,
                "modalidad": modalidad_map.get(s["game_mode_id"], f"ID {s['game_mode_id']}"),
                "escenario": mapa_map.get(s["map_id"], f"Mapa {s['map_id']}"),
                "fecha": s["reservation_date"],
                "hora": f"{s['start_time'][:5]} - {s['end_time'][:5]}",
                "precio": sala_precio,
                "actuales": current,
                "maximos": maximos,
                "estado": "Abierta" if current < maximos else "Llena",
                "game_mode_id": s["game_mode_id"],
                "map_id": s["map_id"],
                "equipment_kit_id": 1,
                "reservation_date": s["reservation_date"],
                "start_time": s["start_time"],
                "end_time": s["end_time"],
                "unido": unido,
                "equipamiento": "Kit Basico",
                "admin_account_id": s.get("admin_account_id"),
                "es_admin_sala": es_admin_sala,
                "es_propia": es_admin_sala and s.get("admin_account_id") == usuario["id"],
            })
            reservas_json.append({
                "map_id": s["map_id"],
                "reservation_date": s["reservation_date"],
                "start_time": s["start_time"],
                "end_time": s["end_time"],
            })

        return render_template('lobby_user.html', salas=salas, usuario=usuario,
                               modalidades=modalidades_admin, mapas=mapas_admin,
                               today=date.today().isoformat(), reservas_json=reservas_json,
                               slot_map=slot_map_dict)

    @app.route("/api/turnos-disponibles")
    def api_turnos_disponibles():
        fecha_param = request.args.get('date')
        if fecha_param:
            try:
                fecha = date.fromisoformat(fecha_param)
            except ValueError:
                return {"error": "Formato de fecha invalido"}, 400
        else:
            fecha = date.today()
        frec = get_frecuencia_horaria(fecha)
        slots = [
            {"id": "cs", "label": "5 - 7", "ocupados": frec.get("cs", 0), "max": 4},
            {"id": "so", "label": "7 - 9", "ocupados": frec.get("so", 0), "max": 4},
            {"id": "nd", "label": "9 - 11", "ocupados": frec.get("nd", 0), "max": 4},
            {"id": "od", "label": "11 - 13", "ocupados": frec.get("od", 0), "max": 4},
            {"id": "tc", "label": "13 - 15", "ocupados": frec.get("tc", 0), "max": 4},
            {"id": "qs", "label": "15 - 17", "ocupados": frec.get("qs", 0), "max": 4},
            {"id": "do", "label": "17 - 19", "ocupados": frec.get("do", 0), "max": 4},
            {"id": "dv", "label": "19 - 21", "ocupados": frec.get("dv", 0), "max": 4},
        ]
        for s in slots:
            s["disponible"] = s["ocupados"] < s["max"]
        return {"fecha": fecha.isoformat(), "turnos": slots}

    @app.route("/lobby-privada", methods=['GET', 'POST'])
    def lobby_privada():
        usuario = session.get('usuario')
        if not usuario:
            flash("Debes iniciar sesion para realizar una reserva.", "warning")
            return redirect(url_for('login_sesion'))

        if request.method == 'POST':
            game_mode_id = request.form.get("modalidad")
            map_id = request.form.get("campo")
            equipment_kit_id = request.form.get("pack")
            reservation_date = request.form.get("fecha")
            turno = request.form.get("turno")
            precio = request.form.get("precio")

            if not all([game_mode_id, map_id, equipment_kit_id, reservation_date, turno, precio]):
                flash("Completa todos los campos.", "warning")
                return redirect(url_for('lobby_privada'))

            start_time, end_time = slot_map_dict.get(turno, (None, None))
            if not start_time:
                flash("Selecciona un turno valido.", "warning")
                return redirect(url_for('lobby_privada'))

            try:
                kit_id = int(equipment_kit_id)
            except ValueError:
                flash("Selecciona un pack de equipamiento valido", "warning")
                return redirect(url_for('lobby_privada'))

            modalidades = _api_get_gamemodes()
            modalidad_max_players = 4
            if not isinstance(modalidades, Exception):
                for m in modalidades:
                    if str(m["id"]) == game_mode_id:
                        modalidad_max_players = m.get("players", 4)
                        break

            sala_payload = {
                "game_mode_id": int(game_mode_id),
                "map_id": int(map_id),
                "price": int(precio),
                "reservation_date": reservation_date,
                "start_time": start_time,
                "end_time": end_time,
                "max_players": modalidad_max_players,
                "admin_account_id": int(usuario["id"]),
                "account_id": int(usuario["id"]),
                "join_equipment_kit_id": kit_id,
                "is_public": False,
            }
            sala_resp = _api_post("/salas/", data=sala_payload, token=usuario.get('token'))
            if sala_resp is None:
                flash("No se pudo conectar con el servidor.", "warning")
                return redirect(url_for('lobby_privada'))

            if sala_resp.status_code == 201:
                return redirect(url_for('mensaje_crea_sala_privada'))
            else:
                try:
                    body = sala_resp.json()
                    msg = body.get("message", "No se pudo crear la sala privada.")
                except Exception:
                    msg = "No se pudo crear la sala privada."
                flash(msg, "warning")
                return redirect(url_for('lobby_user'))

        import calendar as calmod
        hoy = date.today()
        primer_dia = date(hoy.year, hoy.month, 1)
        inicio_calendario = primer_dia - timedelta(days=primer_dia.weekday())
        mes_actual = []
        for i in range(35):
            d = inicio_calendario + timedelta(days=i)
            mes_actual.append({'num': d.day, 'fecha': d.isoformat(), 'actual': d.month == hoy.month})
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return render_template('lobby_privada.html',
                               usuario=session.get('usuario'),
                               mes_actual=mes_actual,
                               hoy_str=hoy.isoformat(),
                               mes_nombre=meses[hoy.month - 1],
                               anio=hoy.year,
                               modalidades=_api_get_gamemodes(),
                               mapas=_api_get_maps())

    @app.route('/mensaje_crea_sala_privada')
    def mensaje_crea_sala_privada():
        return render_template('mensaje_crea_sala_privada.html', usuario=session.get('usuario'))
