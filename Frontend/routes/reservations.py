from datetime import date
from flask import flash, render_template, request, redirect, url_for, session
from helpers import (
    slot_map, salas_publicas,
    _api_get_gamemodes, _api_get_maps, _api_get_equipmentkits, _api_post,
    get_frecuencia_horaria, MAX_RESERVAS_POR_DIA
)


def register(app):

    @app.route("/reservas")
    def reservas():
        return render_template('reservas.html', usuario=session.get('usuario'))

    @app.route("/perfil/reservasadmin/crearsala", methods=['GET', 'POST'])
    def admin_crearsala():
        if request.method == 'POST':
            nueva_partida = {
                "id": request.form.get("id_reserva"),
                "modalidad": request.form.get("modalidad"),
                "escenario": request.form.get("escenario"),
                "fecha": request.form.get("fecha"),
                "hora": request.form.get("hora"),
                "actuales": 0,
                "maximos": 10,
                "estado": "[ RESERVA DE ADMIN ]",
            }
            salas_publicas.append(nueva_partida)
            return redirect(url_for('lobby_admin'))
        return render_template('admin_creacionsalapublica.html', modalidades=_api_get_gamemodes())

    @app.route("/perfil/reservasadmin/eliminar/<string:id_partida>", methods=["POST"])
    def eliminar_sala(id_partida):
        salas_publicas[:] = [sala for sala in salas_publicas if sala["id"] != id_partida]
        if "unidas" in session and id_partida in session["unidas"]:
            session["unidas"].remove(id_partida)
            session.modified = True
        return redirect(url_for("lobby_admin"))

    @app.route("/lobby/unirse/<string:id_partida>", methods=["POST"])
    def unirse_sala(id_partida):
        if "unidas" not in session:
            session["unidas"] = []
        if id_partida not in session["unidas"]:
            for sala in salas_publicas:
                if sala["id"] == id_partida and sala["actuales"] < sala["maximos"]:
                    sala["actuales"] += 1
                    session["unidas"].append(id_partida)
                    session.modified = True
                    break
        return redirect(url_for("lobby_admin"))

    @app.route("/lobby-admin")
    def lobby_admin():
        usuario = session.get('usuario')
        mis_unidas = session.get("unidas", [])
        if not usuario:
            flash("Debes iniciar sesión para acceder a las salas públicas.", "warning")
            return redirect(url_for('login_sesion'))
        return render_template('lobby_admin.html', salas=salas_publicas, unidas=mis_unidas, usuario=session.get('usuario'))

    @app.route("/lobby_user")
    def lobby_user():
        usuario = session.get('usuario')
        mis_unidas = session.get("unidas", [])
        if not usuario:
            flash("Debes iniciar sesión para acceder a las salas públicas.", "warning")
            return redirect(url_for('login_sesion'))
        return render_template('lobby_user.html', salas=salas_publicas, unidas=mis_unidas, usuario=usuario)

    @app.route("/lobby-privada", methods=['GET', 'POST'])
    def lobby_privada():
        usuario = session.get('usuario')
        if not usuario:
            flash("Debes iniciar sesión para realizar una reserva.", "warning")
            return redirect(url_for('login_sesion'))

        if request.method == 'POST':
            game_mode_id = request.form.get("modalidad")
            map_id = request.form.get("campo")
            equipment_kit_id = request.form.get("pack")
            reservation_date = request.form.get("fecha")
            turno = request.form.get("turno")
            precio = request.form.get("precio")

            if not all([game_mode_id, map_id, equipment_kit_id, reservation_date, turno, precio]):
                flash("Completá todos los campos.", "warning")
                return redirect(url_for('lobby_privada'))

            start_time, end_time = slot_map.get(turno, (None, None))
            if not start_time:
                flash("Seleccioná un turno válido.", "warning")
                return redirect(url_for('lobby_privada'))

            try:
                kit_id = int(equipment_kit_id)
            except ValueError:
                flash("Seleccioná un pack de equipamiento válido", "warning")
                return redirect(url_for('lobby_privada'))

            payload = {
                "account_id": int(usuario["id"]),
                "map_id": int(map_id),
                "equipment_kit_id": kit_id,
                "price": int(precio),
                "reservation_date": reservation_date,
                "start_time": start_time,
                "end_time": end_time,
            }
            resp = _api_post(f"/reservations/{game_mode_id}", data=payload, token=usuario.get('token'))
            if resp is None:
                flash("No se pudo conectar con el servidor.", "warning")
                return redirect(url_for('lobby_privada'))

            if resp.status_code == 200:
                return redirect(url_for('mensaje_crea_sala_privada'))
            elif resp.status_code == 401:
                flash("Tu sesión expiró. Volvé a iniciar sesión.", "warning")
                return redirect(url_for('login_sesion'))
            else:
                try:
                    msg = resp.json().get("message", "No se pudo completar la reserva.")
                except Exception:
                    msg = "No se pudo completar la reserva."
                flash(msg, "warning")
                return redirect(url_for('lobby_privada'))

        from datetime import timedelta
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
                               mapas=_api_get_maps(),
                               pack=_api_get_equipmentkits())

    @app.route("/api/turnos-disponibles")
    def api_turnos_disponibles():
        fecha_param = request.args.get('date')
        if fecha_param:
            try:
                fecha = date.fromisoformat(fecha_param)
            except ValueError:
                return {"error": "Formato de fecha inválido"}, 400
        else:
            fecha = date.today()
        try:
            frec = get_frecuencia_horaria(fecha)
        except Exception:
            frec = {'cs': 0, 'so': 0, 'nd': 0, 'od': 0, 'tc': 0, 'qs': 0, 'do': 0, 'dv': 0}
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

    @app.route('/mensaje_crea_sala_privada')
    def mensaje_crea_sala_privada():
        return render_template('mensaje_crea_sala_privada.html', usuario=session.get('usuario'))
