from datetime import date
from flask import flash, render_template, request, redirect, url_for, session
from helpers import (
    REVIEWS_PER_PAGE, EQUIP_PER_PAGE, USUARIOS_PER_PAGE,
    _api_get_maps, _api_get_gamemodes, _api_get_equipment_kit,
    _api_get, _api_post, _api_put, _api_patch, _api_delete,
    get_reservas_dia, contar_reservas_dia, get_ingresos_periodo,
    get_frecuencia_horaria, get_calendario_mes, MAX_RESERVAS_POR_DIA
)


def register(app):

    @app.route("/admin_panel")
    def admin_panel():
        return render_template("admin_panel.html", usuario=session.get("usuario"))

    @app.route("/admin_dashboard", methods=["GET"])
    def admin_dashboard():
        hoy = date.today()
        try:
            reservas = get_reservas_dia(hoy, limit=100, offset=0)
            total_ocupadas = contar_reservas_dia(hoy)
        except Exception:
            reservas = []
            total_ocupadas = 0

        reservas_dis = [{
            "id_reserva": "-", "user_name": "-", "dni_usuario": "-",
            "price": "-", "start_time": "-", "end_time": "-", "map_name": "-",
        } for _ in range(max(0, MAX_RESERVAS_POR_DIA - total_ocupadas))]

        try:
            cantidad = get_ingresos_periodo(hoy)
        except Exception:
            cantidad = {'dia': 0, 'semana': 0, 'mes': 0, 'año': 0}

        try:
            frec_reservas = get_frecuencia_horaria(hoy)
        except Exception:
            frec_reservas = {'cs': 0, 'so': 0, 'nd': 0, 'od': 0, 'tc': 0, 'qs': 0, 'do': 0, 'dv': 0}

        try:
            mes_actual, hoy_str, mes_nombre, anio = get_calendario_mes()
        except Exception:
            from datetime import timedelta
            import calendar
            primer_dia = date(hoy.year, hoy.month, 1)
            inicio_calendario = primer_dia - timedelta(days=primer_dia.weekday())
            mes_actual = [{'num': d.day, 'fecha': d.isoformat(), 'actual': d.month == hoy.month}
                          for d in [inicio_calendario + timedelta(days=i) for i in range(35)]]
            hoy_str = hoy.isoformat()
            meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            mes_nombre = meses[hoy.month - 1]
            anio = hoy.year

        return render_template(
            "admin_dashboard.html",
            cantidad=cantidad, mes_actual=mes_actual, hoy_str=hoy_str,
            mes_nombre=mes_nombre, anio=anio, data_ocu=reservas,
            data_dis=reservas_dis, frec_reservas=frec_reservas,
            total_ocupadas=total_ocupadas, total_slots=MAX_RESERVAS_POR_DIA,
        )

    @app.route("/api/dashboard/data")
    def api_dashboard_data():
        fecha_param = request.args.get('date')
        if fecha_param:
            try:
                fecha = date.fromisoformat(fecha_param)
            except ValueError:
                return {"error": "Formato de fecha inválido"}, 400
        else:
            fecha = date.today()
        try:
            reservas = get_reservas_dia(fecha, limit=100, offset=0)
            total_ocupadas = contar_reservas_dia(fecha)
        except Exception:
            reservas = []
            total_ocupadas = 0
        reservas_dis = [{"id_reserva": "-", "user_name": "-", "dni_usuario": "-",
                         "price": "-", "start_time": "-", "end_time": "-", "map_name": "-"}
                        for _ in range(max(0, MAX_RESERVAS_POR_DIA - total_ocupadas))]
        try:
            cantidad = get_ingresos_periodo(fecha)
            cantidad_serializable = {k: int(v) for k, v in cantidad.items()}
        except Exception:
            cantidad_serializable = {'dia': 0, 'semana': 0, 'mes': 0, 'año': 0}
        try:
            frec = get_frecuencia_horaria(fecha)
        except Exception:
            frec = {'cs': 0, 'so': 0, 'nd': 0, 'od': 0, 'tc': 0, 'qs': 0, 'do': 0, 'dv': 0}
        return {
            "reservas": reservas, "disponibles": reservas_dis,
            "ingresos": cantidad_serializable, "frecuencia": frec,
            "total_ocupadas": total_ocupadas, "total_slots": MAX_RESERVAS_POR_DIA,
        }

    @app.route("/panel_admin/administrar_usuarios")
    def admin_usuarios():
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        if not usuario.get("is_admin"):
            flash("No tenés permisos de administrador", "warning")
            return redirect(url_for('index'))

        page = max(1, request.args.get('page', 1, type=int))
        offset = (page - 1) * USUARIOS_PER_PAGE
        listusuarios = []
        total = 0
        resp = _api_get("/account/", params={"_offset": offset, "_limit": USUARIOS_PER_PAGE})
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
        elif resp.status_code == 200:
            data = resp.json()
            listusuarios = data.get('Listado de Usuarios', [])
            total = data.get("total", 0)
        else:
            flash("No se pudo obtener la lista de los usuarios.", "warning")
        total_pages = max(1, (total + USUARIOS_PER_PAGE - 1) // USUARIOS_PER_PAGE)
        return render_template("admin_usuarios.html", usuario=usuario, usuarios=listusuarios, page=page, total_pages=total_pages)

    @app.route('/admin_usuario/toggle_estado', methods=['POST'])
    def toggle_usuario_estado():
        usuario = session.get('usuario')
        if not usuario or not usuario.get("is_admin"):
            flash("No tenés permisos de administrador", "warning")
            return redirect(url_for('index'))

        user_id = request.form.get("id_usuario")
        nuevo_estado = 0 if int(request.form.get("estado_actual")) == 1 else 1
        resp = _api_patch(f"/account/{user_id}/toggle_status", data={"is_active": nuevo_estado})
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
        elif resp.status_code == 204:
            flash("Estado del usuario actualizado.", "success")
        else:
            flash("Error al cambiar el estado.", "warnig")
        return redirect(url_for('admin_usuarios'))

    @app.route('/admin_usuario/editar/<int:id_usuario_edit>', methods=['GET', 'POST'])
    def admin_usuarios_editar(id_usuario_edit):
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        if not usuario.get("is_admin"):
            flash("No tenés permisos de administrador", "warning")
            return redirect(url_for('index'))

        datos_usuario = None
        resp = _api_get(f"/account/{id_usuario_edit}")
        if resp and resp.status_code == 200:
            datos_usuario = resp.json().get('Cuenta')
        else:
            flash("No se pudo obtener la lista de los usuarios.", "warning")

        if request.method == "POST":
            datos_actualizados = {
                "username": request.form.get("username"),
                "email": request.form.get("email"),
                "elo": request.form.get("elo"),
                "phone": request.form.get("phone"),
                "about_me": request.form.get("about_me"),
                "password": request.form.get("password"),
                "is_active": int(request.form.get("is_active", 0))
            }
            resp = _api_patch(f"/account/{id_usuario_edit}", data=datos_actualizados)
            if resp is None:
                flash("No se pudo conectar con el servidor.", "warning")
                return redirect(url_for("admin_panel"))
            if resp.status_code == 204:
                flash("Los datos del usuario fueron actualizados exitosamente.", "success")
            elif resp.status_code in (401, 403):
                flash("No autorizado para actualizar datos de usuarios.", "warning")
            else:
                flash("No se pudo actualizar los datos del usuario.", "warning")
            return redirect(url_for("admin_panel"))

        return render_template("admin_usuarios_editar.html", id_usuario_edit=id_usuario_edit, usuario=usuario, datos=datos_usuario)

    @app.route('/admin_servicios', methods=['GET', 'POST'])
    def admin_servicios():
        servicios_db = [
            {"id": 1, "nombre": "Bufet / Bar", "descripcion": "Venta de bebidas y comidas post-partido."},
            {"id": 2, "nombre": "Estacionamiento", "descripcion": "Predio cerrado con seguridad para autos y motos."}
        ]
        if request.method == 'POST':
            nuevo_nombre = request.form.get('nombre')
            nueva_desc = request.form.get('descripcion')
            nuevo_id = len(servicios_db) + 1
            servicios_db.append({"id": nuevo_id, "nombre": nuevo_nombre, "descripcion": nueva_desc})
            return render_template('admin_servicios.html', servicios=servicios_db, usuario=session.get('usuario'))
        return render_template('admin_servicios.html', servicios=servicios_db, usuario=session.get('usuario'))

    @app.route('/admin_equipamiento', methods=['GET', 'POST'])
    def admin_equipamiento():
        if request.method == "POST":
            payload = {
                "name": request.form.get("name"),
                "brand": request.form.get("brand"),
                "price": request.form.get("price"),
                "quantity": request.form.get("quantity", 1),
                "purchase_link": request.form.get("purchase_link"),
            }
            resp = _api_post("/equipmentkit/", data=payload)
            if resp is None:
                flash("No se pudo conectar con el servidor.", "warning")
            elif resp.status_code == 201:
                flash("Equipamiento registrado.", "success")
            else:
                flash("No se pudo registrar el equipamiento.", "warning")
            return redirect(url_for('admin_equipamiento'))

        page = max(1, request.args.get('page', 1, type=int))
        offset = (page - 1) * EQUIP_PER_PAGE
        equipamiento = []
        total = 0
        resp = _api_get("/equipmentkit/", params={"_offset": offset, "_limit": EQUIP_PER_PAGE})
        if resp and resp.status_code == 200:
            data = resp.json()
            equipamiento = data.get('equipmentkits', [])
            total = data.get('total', 0)
        else:
            flash("No se pudo conectar con el servidor.", "warning")
        total_pages = max(1, (total + EQUIP_PER_PAGE - 1) // EQUIP_PER_PAGE)
        return render_template('admin_equipamiento.html', equipamiento=equipamiento,
                               usuario=session.get('usuario'), page=page, total_pages=total_pages)

    @app.route('/admin_equipamiento/modificar/<int:kit_id>', methods=['POST'])
    def modificar_equipamiento(kit_id):
        payload = {
            "name": request.form.get("name"),
            "brand": request.form.get("brand"),
            "price": request.form.get("price"),
            "quantity": request.form.get("quantity", 1),
            "purchase_link": request.form.get("purchase_link"),
        }
        resp = _api_put(f"/equipmentkit/{kit_id}", data=payload)
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
        elif resp.status_code == 200:
            flash("Equipamiento actualizado.", "success")
        else:
            flash("No se pudo actualizar el equipamiento.", "warning")
        return redirect(url_for('admin_equipamiento'))

    @app.route('/admin_equipamiento/eliminar/<int:kit_id>', methods=['POST'])
    def eliminar_equipamiento(kit_id):
        resp = _api_delete(f"/equipmentkit/{kit_id}")
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
        else:
            flash("Equipamiento eliminado.", "success")
        return redirect(url_for('admin_equipamiento'))

    @app.route('/admin_equipamiento/info/<int:kit_id>', methods=['GET', 'POST'])
    def admin_equipamiento_info(kit_id):
        if request.method == "POST":
            link = request.form.get("purchase_link")
            kit = _api_get_equipment_kit(kit_id)
            if not kit:
                flash("Equipamiento no encontrado.", "warning")
                return redirect(url_for('admin_equipamiento'))
            payload = {
                "name": kit["name"], "brand": kit["brand"], "price": kit["price"],
                "quantity": kit["quantity"], "purchase_link": link,
            }
            resp = _api_put(f"/equipmentkit/{kit_id}", data=payload)
            if resp is None:
                flash("No se pudo conectar con el servidor.", "warning")
            elif resp.status_code == 200:
                flash("Link de compra actualizado.", "success")
            else:
                flash("No se pudo actualizar el link.", "warning")
            return redirect(url_for('admin_equipamiento_info', kit_id=kit_id))

        kit = _api_get_equipment_kit(kit_id)
        if not kit:
            flash("Equipamiento no encontrado.", "warning")
            return redirect(url_for('admin_equipamiento'))
        return render_template('admin_equipamiento_info.html', kit=kit, usuario=session.get('usuario'))

    @app.route("/admin_resenias")
    def admin_resenias():
        usuario = session.get("usuario")
        if not usuario or not usuario.get("is_admin"):
            flash("Acceso solo para administradores.", "warning")
            return redirect(url_for("login_sesion"))
        page = max(1, request.args.get('page', 1, type=int))
        offset = (page - 1) * REVIEWS_PER_PAGE
        token = usuario.get('token')
        mapas = {m["id"]: m["name"] for m in _api_get_maps()}
        resenias = []
        total = 0
        resp = _api_get("/reviews/", params={"_offset": offset, "_limit": REVIEWS_PER_PAGE}, token=token)
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
        elif resp.status_code == 200:
            data = resp.json()
            total = data.get("total", 0)
            for r in data.get("reviews", []):
                resenias.append({
                    "id": r["id"], "usuario": "Jugador",
                    "mapa": mapas.get(r["map_id"], "Desconocido"),
                    "puntuacion": r["stars"], "titulo": "Reseña de la comunidad",
                    "comentario": r.get("body_review", ""),
                    "approved": r.get("approved", False),
                })
        elif resp.status_code == 401:
            flash("Tu sesión expiró. Volvé a iniciar sesión.", "warning")
            return redirect(url_for("login_sesion"))
        total_pages = max(1, (total + REVIEWS_PER_PAGE - 1) // REVIEWS_PER_PAGE)
        return render_template("admin_resenias.html", resenias=resenias, usuario=usuario,
                               page=page, total_pages=total_pages)

    @app.route("/admin_resenias/moderar/<int:resena_id>", methods=["POST"])
    def moderar_resenia(resena_id):
        usuario = session.get("usuario")
        if not usuario or not usuario.get("is_admin"):
            flash("Acceso solo para administradores.", "warning")
            return redirect(url_for("login_sesion"))
        approved = request.form.get("approved") == "true"
        resp = _api_patch(f"/reviews/auth/{resena_id}", data={"approved": approved}, token=usuario.get('token'))
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
        elif resp.status_code == 200:
            flash("Reseña aprobada." if approved else "Reseña desaprobada.", "success")
        elif resp.status_code in (401, 403):
            flash("No autorizado para moderar reseñas.", "warning")
        else:
            flash("No se pudo actualizar la reseña.", "warning")
        return redirect(url_for("admin_resenias"))

    @app.route("/admin/modalidades/crear", methods=['GET', 'POST'])
    def admin_modalidades_crear():
        usuario = session.get('usuario')
        if not usuario or not usuario.get('is_admin'):
            flash("Acceso solo para administradores.", "warning")
            return redirect(url_for('modalidades'))
        if request.method == 'POST':
            name = request.form.get('name')
            duration = request.form.get('duration')
            players = request.form.get('players')
            description = request.form.get('description')
            resp = _api_post("/gamemodes/", data={
                'name': name, 'duration': duration, 'players': int(players), 'description': description
            })
            if resp is None:
                flash("Error de conexión con el servidor.", "warning")
            elif resp.status_code == 201:
                flash("Modalidad creada exitosamente.", "warning")
            else:
                flash("Error al crear la modalidad.", "warning")
            return redirect(url_for('modalidades'))
        return render_template('admin_modalidades_crear.html', usuario=usuario)

    @app.route("/admin/modalidades/editar/<int:id>", methods=['GET', 'POST'])
    def admin_modalidades_editar(id):
        usuario = session.get('usuario')
        if not usuario or not usuario.get('is_admin'):
            flash("Acceso solo para administradores.", "warning")
            return redirect(url_for('modalidades'))
        modo = next((m for m in _api_get_gamemodes() if m['id'] == id), None)
        if not modo:
            flash("Modalidad no encontrada.", "warning")
            return redirect(url_for('modalidades'))
        if request.method == 'POST':
            name = request.form.get('name')
            duration = request.form.get('duration')
            players = request.form.get('players')
            description = request.form.get('description')
            resp = _api_put(f"/gamemodes/{id}", data={
                'name': name, 'duration': duration, 'players': int(players), 'description': description
            })
            if resp is None:
                flash("Error de conexión con el servidor.", "warning")
            elif resp.status_code == 200:
                map_ids = request.form.getlist('map_ids')
                _api_put(f"/gamemodes/{id}/maps", data={'map_ids': map_ids})
                flash("Modalidad actualizada exitosamente.", "success")
            else:
                flash("Error al actualizar la modalidad.", "warning")
            return redirect(url_for('modalidades'))
        return render_template('admin_modalidades_editar.html', modo=modo, usuario=usuario, mapas=_api_get_maps())

    @app.route("/admin/modalidades/eliminar/<int:id>", methods=['POST'])
    def admin_modalidades_eliminar(id):
        usuario = session.get('usuario')
        if not usuario or not usuario.get('is_admin'):
            flash("Acceso solo para administradores.", "warning")
            return redirect(url_for('modalidades'))
        resp = _api_delete(f"/gamemodes/{id}")
        if resp is None:
            flash("Error de conexión con el servidor.", "warning")
        elif resp.status_code == 200:
            flash("Modalidad eliminada exitosamente.", "success")
        else:
            flash("Error al eliminar la modalidad.", "warning")
        return redirect(url_for('modalidades'))
