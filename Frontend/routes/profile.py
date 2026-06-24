import os
from flask import flash, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from helpers import (
    REVIEWS_PER_PAGE, _api_get, _api_post, _api_patch,
)
from services.public_services import _api_get_maps, _api_get_gamemodes
from services.public_services import _api_send_contact_message


def _get_user_history(user_id, token):
    salas_resp = _api_get("/salas/", params={"_limit": 1000}, token=token)
    reservas_resp = _api_get("/reservations/", params={"_limit": 1000}, token=token)

    modalidades = _api_get_gamemodes()
    modalidad_map = {}
    if not isinstance(modalidades, Exception):
        modalidad_map = {m["id"]: m["name"] for m in modalidades}

    mapas = _api_get_maps()
    mapa_map = {}
    if not isinstance(mapas, Exception):
        mapa_map = {m["id"]: m["name"] for m in mapas}

    all_salas = []
    if salas_resp and salas_resp.status_code == 200:
        all_salas = salas_resp.json().get("salas", [])

    all_reservas = []
    if reservas_resp and reservas_resp.status_code == 200:
        all_reservas = reservas_resp.json().get("reservas", [])

    user_reservas = [r for r in all_reservas if r.get("account_id") == user_id and not r.get("canceled")]
    user_sala_ids = {r["sala_id"] for r in user_reservas}

    history = []
    for s in all_salas:
        if s.get("canceled"):
            continue
        is_owner = s.get("admin_account_id") == user_id
        is_joined = s["id"] in user_sala_ids
        if not is_owner and not is_joined:
            continue
        user_res = None
        for r in user_reservas:
            if r["sala_id"] == s["id"]:
                user_res = r
                break
        kit_name = "Kit Basico" if user_res else "-"
        history.append({
            "id": s["id"],
            "tipo": "Privada" if not s.get("is_public", True) else "Publica",
            "modalidad": modalidad_map.get(s["game_mode_id"], f"ID {s['game_mode_id']}"),
            "mapa": mapa_map.get(s["map_id"], f"Mapa {s['map_id']}"),
            "fecha": s["reservation_date"],
            "horario": f"{s['start_time'][:5]} - {s['end_time'][:5]}",
            "equipamiento": kit_name,
            "precio": user_res["price"] if user_res else s.get("price", 0),
        })
    return history


def register(app):

    @app.route('/perfil')
    def perfil():
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        old_picture = usuario.get('profile_picture')
        cuenta_resp = _api_get(f"/account/{usuario['id']}", token=usuario.get('token'))
        if cuenta_resp and cuenta_resp.status_code == 200:
            cuenta = cuenta_resp.json().get("Cuenta", {})
            cuenta["user_name"] = cuenta.get("username")
            if old_picture:
                cuenta['profile_picture'] = old_picture
            session['usuario'] = cuenta
            usuario = cuenta
        favoritos = session.get('favoritos', [])
        mapas = _api_get_maps()
        historial = _get_user_history(usuario["id"], usuario.get("token"))
        return render_template('perfil.html', usuario=usuario, favoritos=favoritos, mapas=mapas, historial=historial)

    @app.route('/perfil/favoritos/agregar/<int:map_id>', methods=['POST'])
    def perfil_favoritos_agregar(map_id):
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        favoritos = session.get('favoritos', [])
        if len(favoritos) >= 4:
            flash("Maximo 4 mapas favoritos", "warning")
            return redirect(url_for('perfil'))
        if any(fav['id'] == map_id for fav in favoritos):
            flash("El mapa ya esta en favoritos", "warning")
            return redirect(url_for('perfil'))
        mapas = _api_get_maps()
        mapa = next((m for m in mapas if m['id'] == map_id), None)
        if not mapa:
            flash("Mapa no encontrado", "warning")
            return redirect(url_for('perfil'))
        favoritos.append(mapa)
        session['favoritos'] = favoritos
        flash("Mapa agregado a favoritos", "success")
        return redirect(url_for('perfil'))

    @app.route('/perfil/favoritos/eliminar/<int:map_id>', methods=['POST'])
    def perfil_favoritos_eliminar(map_id):
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        favoritos = session.get('favoritos', [])
        session['favoritos'] = [f for f in favoritos if f['id'] != map_id]
        flash("Mapa eliminado de favoritos", "success")
        return redirect(url_for('perfil'))

    @app.route('/perfil/actualizar', methods=['POST'])
    def perfil_actualizar():
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        payload = {}
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        if email:
            payload['email'] = email
        if phone:
            payload['phone'] = phone
        if not payload:
            flash("No hay campos para actualizar.", "warning")
            return redirect(url_for('perfil'))
        resp = _api_patch(f"/account/{usuario['id']}", data=payload, token=usuario.get('token'))
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
            return redirect(url_for('perfil'))
        if resp.status_code == 204:
            old_picture = usuario.get('profile_picture')
            cuenta_resp = _api_get(f"/account/{usuario['id']}", token=usuario.get('token'))
            if cuenta_resp and cuenta_resp.status_code == 200:
                cuenta = cuenta_resp.json().get("Cuenta", {})
                cuenta["user_name"] = cuenta.get("username")
                if old_picture:
                    cuenta['profile_picture'] = old_picture
                session['usuario'] = cuenta
            flash("Datos actualizados correctamente.", "success")
        else:
            flash("No se pudieron actualizar los datos.", "warning")
        return redirect(url_for('perfil'))

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    def _allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/perfil/foto', methods=['POST'])
    def perfil_foto():
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        if 'foto' not in request.files:
            flash("No se selecciono ningun archivo.", "warning")
            return redirect(url_for('perfil'))
        file = request.files['foto']
        if file.filename == '':
            flash("No se selecciono ningun archivo.", "warning")
            return redirect(url_for('perfil'))
        if not _allowed_file(file.filename):
            flash("Formato de imagen no permitido (usa PNG, JPG, GIF o WebP).", "warning")
            return redirect(url_for('perfil'))
        upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'profile')
        os.makedirs(upload_dir, exist_ok=True)
        filename = secure_filename(f"user_{usuario['id']}_{file.filename}")
        file.save(os.path.join(upload_dir, filename))
        usuario['profile_picture'] = url_for('static', filename=f'uploads/profile/{filename}')
        session['usuario'] = usuario
        flash("Foto de perfil actualizada.", "success")
        return redirect(url_for('perfil'))

    @app.route('/perfil/password', methods=['POST'])
    def perfil_password():
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        password = request.form.get('password')
        resp = _api_patch(f"/account/{usuario['id']}/password", data={"password": password})
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
            return redirect(url_for('perfil'))
        if resp.status_code == 204:
            flash("Contraseña actualizada.", "success")
        else:
            flash("No se pudo actualizar la contraseña.", "warning")
        return redirect(url_for('perfil'))

    @app.route('/perfil/contacto', methods=['GET', 'POST'])
    def contacto():
        if request.method == 'POST':
            data = {
                'user_name': request.form.get('nombre', '').strip(),
                'email': request.form.get('email', '').strip(),
                'message': request.form.get('mensaje', '').strip(),
            }
            if all(data.values()):
                if _api_send_contact_message(data):
                    flash("Mensaje enviado correctamente.", "success")
                else:
                    flash("Error al enviar el mensaje.", "warning")
            else:
                flash("Completa todos los campos.", "warning")
            return redirect(url_for('contacto'))
        return render_template('contacto.html', usuario=session.get('usuario'))

    @app.route('/perfil/resenias')
    def resenias():
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        return render_template('resenias_escribir.html', usuario=usuario,
                               nombre_usuario=usuario["user_name"], mapas=_api_get_maps())

    @app.route("/perfil/resenias/ver-resenias")
    def ver_resenias():
        usuario = session.get("usuario")
        if not usuario:
            flash("Debes iniciar sesion para ver las reseñas.", "warning")
            return redirect(url_for('login_sesion'))

        page = max(1, request.args.get('page', 1, type=int))
        offset = (page - 1) * REVIEWS_PER_PAGE
        mapas = {m["id"]: m["name"] for m in _api_get_maps()}
        resenias = []
        total = 0
        resp = _api_get("/reviews/", params={"approved": "true", "_offset": offset, "_limit": REVIEWS_PER_PAGE})
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
        elif resp.status_code == 200:
            data = resp.json()
            total = data.get("total", 0)
            for r in data.get("reviews", []):
                admin_resp = r.get("admin_response", "")
                respuestas = []
                if admin_resp:
                    respuestas.append({"autor": "Soporte Kinetix", "texto": admin_resp})
                resenias.append({
                    "id": r["id"], "usuario": "Jugador",
                    "mapa": mapas.get(r["map_id"], "Desconocido"),
                    "puntuacion": r["stars"], "titulo": r.get("title", "") or "Reseña de la comunidad",
                    "comentario": r.get("body_review", ""), "respuestas": respuestas,
                })
        total_pages = max(1, (total + REVIEWS_PER_PAGE - 1) // REVIEWS_PER_PAGE)
        return render_template("ver_resenias.html", resenias=resenias,
                               usuario=usuario, nombre_usuario=usuario["user_name"],
                               page=page, total_pages=total_pages)

    @app.route("/guardar-resenia", methods=["POST"])
    def guardar_resenia():
        usuario = session.get('usuario')
        if not usuario:
            flash("Debes iniciar sesion para enviar una reseña.", "warning")
            return redirect(url_for('login_sesion'))

        comentario = request.form.get("comentario")
        puntuacion = request.form.get("puntuacion")
        mapa = request.form.get("mapa")
        titulo = request.form.get("titulo", "").strip()
        if not (comentario and puntuacion and mapa):
            flash("Faltan datos en la reseña.", "warning")
            return redirect(url_for('resenias'))

        payload = {"stars": int(puntuacion), "map_id": int(mapa), "title": titulo, "body_review": comentario}
        resp = _api_post("/reviews/", data=payload)
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
            return redirect(url_for('resenias'))
        if resp.status_code == 201:
            return render_template("mensaje_envia_resenia.html", usuario=usuario)
        flash("No se pudo enviar la reseña.", "warning")
        return redirect(url_for('resenias'))
