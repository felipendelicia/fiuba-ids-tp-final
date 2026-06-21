from flask import flash, render_template, request, redirect, url_for, session
from helpers import REVIEWS_PER_PAGE, _api_get_maps, _api_get, _api_post, _api_patch


def register(app):

    @app.route('/perfil')
    def perfil():
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        favoritos = session.get('favoritos', [])
        mapas = _api_get_maps()
        return render_template('perfil.html', usuario=usuario, favoritos=favoritos, mapas=mapas)

    @app.route('/perfil/favoritos/agregar/<int:map_id>', methods=['POST'])
    def perfil_favoritos_agregar(map_id):
        usuario = session.get('usuario')
        if not usuario:
            return redirect(url_for('login_sesion'))
        favoritos = session.get('favoritos', [])
        if len(favoritos) >= 4:
            flash("Máximo 4 mapas favoritos", "warning")
            return redirect(url_for('perfil'))
        if any(fav['id'] == map_id for fav in favoritos):
            flash("El mapa ya está en favoritos", "warning")
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
            flash("Debes iniciar sesión para ver las reseñas.", "warning")
            return redirect(url_for('login_sesion'))

        page = max(1, request.args.get('page', 1, type=int))
        offset = (page - 1) * REVIEWS_PER_PAGE
        token = usuario.get('token')
        mapas = {m["id"]: m["name"] for m in _api_get_maps()}
        resenias = []
        total = 0
        resp = _api_get("/reviews/", params={"approved": "true", "_offset": offset, "_limit": REVIEWS_PER_PAGE}, token=token)
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
                    "comentario": r.get("body_review", ""), "respuestas": [],
                })
        elif resp.status_code == 401:
            flash("Tu sesión expiró. Volvé a iniciar sesión.", "warning")
            return redirect(url_for('login_sesion'))
        total_pages = max(1, (total + REVIEWS_PER_PAGE - 1) // REVIEWS_PER_PAGE)
        return render_template("ver_resenias.html", resenias=resenias,
                               usuario=usuario, nombre_usuario=usuario["user_name"],
                               page=page, total_pages=total_pages)

    @app.route("/guardar-resenia", methods=["POST"])
    def guardar_resenia():
        usuario = session.get('usuario')
        if not usuario:
            flash("Debes iniciar sesión para enviar una reseña.", "warning")
            return redirect(url_for('login_sesion'))

        comentario = request.form.get("comentario")
        puntuacion = request.form.get("puntuacion")
        mapa = request.form.get("mapa")
        if not (comentario and puntuacion and mapa):
            flash("Faltan datos en la reseña.", "warning")
            return redirect(url_for('resenias'))

        payload = {"stars": int(puntuacion), "map_id": int(mapa), "body_review": comentario}
        resp = _api_post("/reviews/", data=payload, token=usuario.get('token'))
        if resp is None:
            flash("No se pudo conectar con el servidor.", "warning")
            return redirect(url_for('resenias'))
        if resp.status_code == 201:
            return render_template("mensaje_envia_resenia.html", usuario=usuario)
        if resp.status_code == 401:
            flash("Tu sesión expiró. Volvé a iniciar sesión.", "warning")
            return redirect(url_for('login_sesion'))
        flash("No se pudo enviar la reseña.", "warning")
        return redirect(url_for('resenias'))
