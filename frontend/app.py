from flask import Flask, flash, render_template, request, redirect, url_for, session
from datetime import date, datetime
import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
REVIEWS_PER_PAGE = 2
EQUIP_PER_PAGE = 5
MAPS_PER_PAGE = 10

try:
    from services.dashboard_services import (
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


app = Flask(__name__)
app.secret_key = 'kinetix_clave_super_secreta_para_las_sesiones'


def _fetch_usuario(user_id):
    try:
        resp = requests.get(f"{BACKEND_URL}/account/{user_id}", timeout=5)
    except requests.RequestException:
        return None
    if resp.status_code != 200:
        return None
    cuenta = resp.json().get("Cuenta", {})
    cuenta["user_name"] = cuenta.get("username")
    return cuenta


def _fetch_maps():
    try:
        resp = requests.get(f"{BACKEND_URL}/maps/disponibility?_limit=100", timeout=5)
        if resp.status_code == 200:
            return resp.json().get("Maps", [])
    except requests.RequestException:
        pass
    return []

def _fetch_gamemodes():
    try:
        resp = requests.get(f"{BACKEND_URL}/gamemodes/", timeout=5)
        if resp.status_code == 200:
            return resp.json().get("gamemodes", [])
    except requests.RequestException:
        pass
    return []

def _fetch_equipmentkits():
    try:
        resp = requests.get(f"{BACKEND_URL}/equipmentkit/", timeout=5)
        if resp.status_code == 200:
            return resp.json().get("equipmentkits", [])
    except requests.RequestException:
        pass
    return []




# 1. Ruta para la página principal
@app.route("/")
def index():
    return render_template('index.html', usuario=session.get('usuario'))  

# 2. Ruta para que un usuario pueda Iniciar Sesion
@app.route('/login/sesion', methods=['GET', 'POST'])
def login_sesion():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        recuerdame = request.form.get("recuerdame")

        try:
            resp = requests.post(f"{BACKEND_URL}/authentication/login",
                                 json={"email": email, "password": password}, timeout=5)
        except requests.RequestException:
            flash("No se pudo conectar con el servidor.", "warning")
            return render_template('login_sesion.html')

        if resp.status_code == 200:
            data = resp.json()
            usuario = _fetch_usuario(data["user_id"])
            if usuario:
                usuario["token"] = data.get("token")
                if recuerdame:
                    session.permanent = True
                session['usuario'] = usuario
                return redirect(url_for('perfil'))
            flash("No se pudo obtener el perfil del usuario.", "warning")
        else:
            flash("Usuario o contraseña inválidos.", "warning")

    return render_template('login_sesion.html')

# 3. Ruta para la página de Registrar Nuevo Usuario
@app.route('/login/registro', methods=['GET', 'POST'])
def login_registro():
    if request.method == 'POST':
        payload = {
            "name": request.form.get('name'),
            "username": request.form.get('user_name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "dni": request.form.get('dni'),
            "phone": request.form.get('phone'),
        }
        try:
            resp = requests.post(f"{BACKEND_URL}/authentication/register",
                                 json=payload, timeout=5)
        except requests.RequestException:
            flash("No se pudo conectar con el servidor.", "warning")
            return render_template('login_registro.html')

        if resp.status_code == 201:
            flash("Registro exitoso. Iniciá sesión.", "success")
            return redirect(url_for('login_sesion'))

        msg = "No se pudo completar el registro."
        try:
            msg = resp.json()["errors"][0]["message"]
        except Exception:
            pass
        flash(msg, "warning")
    return render_template('login_registro.html')

# 4. Ruta para la pagína de Recuperación Contraseña de Usuario
@app.route('/login/contrasenia', methods=['GET', 'POST'])
def login_contrasenia():
    email_user = "Bruno@gmail.com"
    if request.method == "POST":
        email = request.form.get("email")
        if email == email_user:
            flash(
                "Hemos enviado un correo con instrucciones de recuperación. Revisa tu bandeja de entrada y la carpeta de spam",
                "success",
            )
            return redirect(url_for('index'))
        else:
            flash("El correo ingresado no coincide con ningún usuario registrado. Verifica tu email e intenta nuevamente.", "warning")
            return render_template('login_contrasenia.html')
    return render_template('login_contrasenia.html')

# 5. Ruta para la página de Campos de Juegos
@app.route("/campos")
def campos():
    return render_template('campos.html', usuario=session.get('usuario'))
@app.route('/campos/informacion/planonuketown')
def info_mapa_index():
    return render_template('nuketown_plano.html', usuario=session.get('usuario'))
@app.route('/campos/informacion/planomirage')
def info_mapa_index2():
    return render_template('mirage_plano.html', usuario=session.get('usuario'))
@app.route('/campos/informacion/planohijacked')
def info_mapa_index3():
    return render_template('hijacked_plano.html', usuario=session.get('usuario'))
@app.route('/campos/informacion/planoterminal')
def info_mapa_index4():
    return render_template('terminal_plano.html', usuario=session.get('usuario'))
@app.route('/campos/informacion/<nombre_mapa>')
def info_mapa(nombre_mapa):
    mapas = {'nuketown': {}, 'mirage': {}, 'hijacked': {}, 'terminal': {}}
    if nombre_mapa not in mapas:
        return render_template('404.html'), 404
    return render_template(f'{nombre_mapa}.html', mapa=mapas[nombre_mapa], usuario=session.get('usuario'))

@app.route('/campos/informacion/<nombre_mapa>/plano')
def info_mapa_plano(nombre_mapa):
    mapas = {'nuketown': {}, 'mirage': {}, 'hijacked': {}, 'terminal': {}}
    if nombre_mapa not in mapas:
        return render_template('404.html'), 404
    return render_template(f'{nombre_mapa}_plano.html', mapa=mapas[nombre_mapa], usuario=session.get('usuario'))

# 6. Ruta para la página de de perfil del usuario
@app.route('/perfil')
def perfil():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('login_sesion'))
    favoritos = session.get('favoritos', [])
    mapas = _fetch_maps()
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
    mapas = _fetch_maps()
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
    try:
        resp = requests.patch(f"{BACKEND_URL}/account/{usuario['id']}/password",
                              json={"password": password}, timeout=5)
    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "warning")
        return redirect(url_for('perfil'))
    if resp.status_code == 204:
        flash("Contraseña actualizada.", "success")
    else:
        flash("No se pudo actualizar la contraseña.", "warning")
    return redirect(url_for('perfil'))

# 7. Ruta para la página Reservas de Campos
@app.route("/reservas")
def reservas():
    return render_template('reservas.html', usuario =session.get('usuario'))

# --- SISTEMA DE GESTIÓN DE SALAS PÚBLICAS ---
salas_publicas = []

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
    return render_template('admin_creacionsalapublica.html', modalidades=_fetch_gamemodes())

@app.route("/perfil/reservasadmin/eliminar/<string:id_partida>", methods=["POST"])
def eliminar_sala(id_partida):
    global salas_publicas
    salas_publicas = [
        sala for sala in salas_publicas if sala["id"] != id_partida
    ]

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
    if  not usuario:
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
# ---------------------------------------------------


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

    payload = {
        "stars": int(puntuacion),
        "map_id": int(mapa),
        "body_review": comentario,
    }
    headers = {"Authorization": f"Bearer {usuario.get('token')}"}
    try:
        resp = requests.post(f"{BACKEND_URL}/reviews/", json=payload, headers=headers, timeout=5)
    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "warning")
        return redirect(url_for('resenias'))

    if resp.status_code == 201:
        return render_template("mensaje_envia_resenia.html", usuario=usuario)
    if resp.status_code == 401:
        flash("Tu sesión expiró. Volvé a iniciar sesión.", "warning")
        return redirect(url_for('login_sesion'))
    flash("No se pudo enviar la reseña.", "warning")
    return redirect(url_for('resenias'))


@app.route("/admin_resenias/moderar/<int:resena_id>", methods=["POST"])
def moderar_resenia(resena_id):
    usuario = session.get("usuario")
    if not usuario or not usuario.get("is_admin"):
        flash("Acceso solo para administradores.", "warning")
        return redirect(url_for("login_sesion"))
    approved = request.form.get("approved") == "true"
    headers = {"Authorization": f"Bearer {usuario.get('token')}"}
    try:
        resp = requests.patch(f"{BACKEND_URL}/reviews/auth/{resena_id}",
                              json={"approved": approved}, headers=headers, timeout=5)
        if resp.status_code == 200:
            flash("Reseña aprobada." if approved else "Reseña desaprobada.", "success")
        elif resp.status_code in (401, 403):
            flash("No autorizado para moderar reseñas.", "warning")
        else:
            flash("No se pudo actualizar la reseña.", "warning")
    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "warning")
    return redirect(url_for("admin_resenias"))


@app.route("/resenias")
def opciones_resenias():
    usuario = session.get('usuario')
    return render_template('resenias_opciones.html', usuario=usuario)

@app.route("/perfil/resenias")
def resenias():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('login_sesion'))
    return render_template('resenias_escribir.html', usuario=usuario,
                           nombre_usuario=usuario["user_name"], mapas=_fetch_maps())


@app.route("/perfil/resenias/ver-resenias")
def ver_resenias():
    usuario = session.get("usuario")
    if not usuario:
        flash("Debes iniciar sesión para ver las reseñas.", "warning")
        return redirect(url_for('login_sesion'))

    page = max(1, request.args.get('page', 1, type=int))
    offset = (page - 1) * REVIEWS_PER_PAGE
    headers = {"Authorization": f"Bearer {usuario.get('token')}"}
    mapas = {m["id"]: m["name"] for m in _fetch_maps()}
    resenias = []
    total = 0
    try:
        resp = requests.get(
            f"{BACKEND_URL}/reviews/?approved=true&_offset={offset}&_limit={REVIEWS_PER_PAGE}",
            headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            total = data.get("total", 0)
            for r in data.get("reviews", []):
                resenias.append({
                    "id": r["id"],
                    "usuario": "Jugador",
                    "mapa": mapas.get(r["map_id"], "Desconocido"),
                    "puntuacion": r["stars"],
                    "titulo": "Reseña de la comunidad",
                    "comentario": r.get("body_review", ""),
                    "respuestas": [],
                })
        elif resp.status_code == 401:
            flash("Tu sesión expiró. Volvé a iniciar sesión.", "warning")
            return redirect(url_for('login_sesion'))
    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "warning")
    total_pages = max(1, (total + REVIEWS_PER_PAGE - 1) // REVIEWS_PER_PAGE)
    return render_template("ver_resenias.html", resenias=resenias,
                           usuario=usuario, nombre_usuario=usuario["user_name"],
                           page=page, total_pages=total_pages)

@app.route("/admin_panel")
def admin_panel():
    return render_template("admin_panel.html", usuario=session.get("usuario"))

@app.route("/admin_resenias")
def admin_resenias():
    usuario = session.get("usuario")
    if not usuario or not usuario.get("is_admin"):
        flash("Acceso solo para administradores.", "warning")
        return redirect(url_for("login_sesion"))
    page = max(1, request.args.get('page', 1, type=int))
    offset = (page - 1) * REVIEWS_PER_PAGE
    headers = {"Authorization": f"Bearer {usuario.get('token')}"}
    mapas = {m["id"]: m["name"] for m in _fetch_maps()}
    resenias = []
    total = 0
    try:
        resp = requests.get(f"{BACKEND_URL}/reviews/?_offset={offset}&_limit={REVIEWS_PER_PAGE}", headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            total = data.get("total", 0)
            for r in data.get("reviews", []):
                resenias.append({
                    "id": r["id"],
                    "usuario": "Jugador",
                    "mapa": mapas.get(r["map_id"], "Desconocido"),
                    "puntuacion": r["stars"],
                    "titulo": "Reseña de la comunidad",
                    "comentario": r.get("body_review", ""),
                    "approved": r.get("approved", False),
                })
        elif resp.status_code == 401:
            flash("Tu sesión expiró. Volvé a iniciar sesión.", "warning")
            return redirect(url_for("login_sesion"))
    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "warning")
    total_pages = max(1, (total + REVIEWS_PER_PAGE - 1) // REVIEWS_PER_PAGE)
    return render_template("admin_resenias.html", resenias=resenias, usuario=usuario,
                           page=page, total_pages=total_pages)

# 10. Ruta para la página de administración de reservas
@app.route("/admin_reservas")
def admin_reservas():
    return render_template('admin_reservas.html', usuario=session.get('usuario'))

# 11. Ruta para la página de Administrador de Servicios
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

# 10. Ruta para la página de Dashboard
@app.route("/admin_dashboard", methods=["GET"])
def admin_dashboard():
    hoy = date.today()

    limit = request.args.get('_limit', 10, type=int)
    offset = request.args.get('_offset', 0, type=int)

    try:
        reservas = get_reservas_dia(hoy, limit=100, offset=0)
        total_ocupadas = contar_reservas_dia(hoy)
    except Exception:
        reservas = []
        total_ocupadas = 0

    reservas_dis = []
    for i in range(max(0, MAX_RESERVAS_POR_DIA - total_ocupadas)):
        reservas_dis.append({
            "id_reserva": "-",
            "user_name": "-",
            "dni_usuario": "-",
            "price": "-",
            "start_time": "-",
            "end_time": "-",
            "map_name": "-",
        })

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
        mes_actual = []
        for i in range(35):
            d = inicio_calendario + timedelta(days=i)
            mes_actual.append({'num': d.day, 'fecha': d.isoformat(), 'actual': d.month == hoy.month})
        hoy_str = hoy.isoformat()
        meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
                 'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        mes_nombre = meses[hoy.month - 1]
        anio = hoy.year

    return render_template(
        "admin_dashboard.html",
        cantidad=cantidad,
        mes_actual=mes_actual,
        hoy_str=hoy_str,
        mes_nombre=mes_nombre,
        anio=anio,
        data_ocu=reservas,
        data_dis=reservas_dis,
        frec_reservas=frec_reservas,
        total_ocupadas=total_ocupadas,
        total_slots=MAX_RESERVAS_POR_DIA,
    )


# 11. API JSON - datos del dashboard por fecha
@app.route("/api/dashboard/data")
def api_dashboard_data():
    from decimal import Decimal
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
        "reservas": reservas,
        "disponibles": reservas_dis,
        "ingresos": cantidad_serializable,
        "frecuencia": frec,
        "total_ocupadas": total_ocupadas,
        "total_slots": MAX_RESERVAS_POR_DIA,
    }

@app.route("/panel_admin/administrar_usuarios")
def admin_usuarios():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('login_sesion'))
    if not usuario.get("is_admin"):
        flash("No tenés permisos de administrador", "warning")
        return redirect(url_for('index'))

    resp = requests.get(f"{BACKEND_URL}/account", timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        listusuarios = data['Listado de Usuarios']
    else:
        listusuarios = []
        flash("No se puedo obtener la lista de los usuarios.", "warning")

    return render_template("admin_usuarios.html", usuario=usuario, usuarios=listusuarios) #pendiente listar-usuarios 

@app.route('/admin_usuario/editar/<int:id_usuario_edit>', methods=['GET', 'POST'])
def admin_usuarios_editar(id_usuario_edit):
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('login_sesion'))
    if not usuario.get("is_admin"):
        flash("No tenés permisos de administrador", "warning")
        return redirect(url_for('index'))

    resp = requests.get(f"{BACKEND_URL}/account/{id_usuario_edit}", timeout=5)
    if resp.status_code == 200:
        usuarios = resp.json()
        datos_usuario = usuarios['Cuenta']
    else:
        usuarios = []
        flash("No se puedo obtener la lista de los usuarios.", "warning")
    
    if request.method == "POST":
        datos_actualizados = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "elo": request.form.get("elo"),
            "phone": request.form.get("phone"),
            "about_me": request.form.get("about_me"), 
            "password": request.form.get("password") or "", # Acá remover el dato de password (?
            "is_active": int(request.form.get("is_active", 0))
            }
        try:
            resp = requests.patch(f"{BACKEND_URL}/account/{id_usuario_edit}",
                                json=datos_actualizados, timeout=5)
            if resp.status_code == 204:
                flash("Los datos del uaurio fueron actualizados exitosamente.", "success")
            elif resp.status_code in (401, 403):
                flash("No autorizado para actualizar datos de usuarios.", "warning")
            else:
                flash("No se pudo actualizar los datos del usuario.", "warning")
        except requests.RequestException:
            flash("No se pudo conectar con el servidor.", "warning")
            return redirect(url_for("admin_panel"))
        return redirect(url_for("admin_panel"))

    return render_template("admin_usuarios_editar.html", id_usuario_edit=id_usuario_edit, usuario=usuario, datos=datos_usuario)

# 13. Ruta para la página de Sala Privada
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

        if not all([game_mode_id, map_id, equipment_kit_id, reservation_date, turno, precio]):
            flash("Completá todos los campos.", "warning")
            return redirect(url_for('lobby_privada'))

        start_time, end_time = slot_map.get(turno, (None, None))
        if not start_time:
            flash("Seleccioná un turno válido.", "warning")
            return redirect(url_for('lobby_privada'))

        '''
        kit_map = {'basico': 1}
        kit_id = kit_map.get(equipment_kit_id)
        if not kit_id:
            flash("Seleccioná un pack de equipamiento válido.", "warning")
            return redirect(url_for('lobby_privada'))
        '''
        try:
            kit_id= int(equipment_kit_id)
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
        headers = {"Authorization": f"Bearer {usuario.get('token')}"}

        try:
            resp = requests.post(f"{BACKEND_URL}/reservations/{game_mode_id}", json=payload, headers=headers, timeout=5)
        except requests.RequestException:
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
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
             'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    return render_template('lobby_privada.html',
                           usuario=session.get('usuario'),
                           mes_actual=mes_actual,
                           hoy_str=hoy.isoformat(),
                           mes_nombre=meses[hoy.month - 1],
                           anio=hoy.year,
                           modalidades=_fetch_gamemodes(),
                           mapas=_fetch_maps(),
                           pack= _fetch_equipmentkits())

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


# 14. Ruta para la página de Servicios
@app.route('/servicios')
def servicios():
    servicios_db = [
        {"id": 1, "nombre": "Bufet / Bar", "descripcion": "Venta de bebidas y comidas post-partido."},
        {"id": 2, "nombre": "Estacionamiento", "descripcion": "Predio cerrado con seguridad para autos y motos."}
    ]
    return render_template('servicios.html', servicios=servicios_db, usuario=session.get('usuario'))

# 16. Ruta para la página de Contacto para usuarios
@app.route('/perfil/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        return redirect(url_for('contacto'))
    return render_template('contacto.html', usuario=session. get('usuario'))

# 17. Ruta para la página de Equipamientos
@app.route('/equipamiento')
def equipamiento():
    return render_template('equipamiento.html' ,usuario=session.get('usuario'))

# 18. Ruta para la página de Equipamientos - Armas
@app.route('/equipamientoinfo/armasinfo')
def equipamiento_armas():
    return render_template('equipamiento_armas.html', usuario=session.get('usuario'))

# 19. Ruta para la página de Equipamientos - Pelotas y Pecheras
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
        try:
            resp = requests.post(f"{BACKEND_URL}/equipmentkit/", json=payload, timeout=5)
            if resp.status_code == 201:
                flash("Equipamiento registrado.", "success")
            else:
                flash("No se pudo registrar el equipamiento.", "warning")
        except requests.RequestException:
            flash("No se pudo conectar con el servidor.", "warning")
        return redirect(url_for('admin_equipamiento'))

    page = max(1, request.args.get('page', 1, type=int))
    offset = (page - 1) * EQUIP_PER_PAGE
    equipamiento = []
    total = 0
    try:
        resp = requests.get(f"{BACKEND_URL}/equipmentkit/?_offset={offset}&_limit={EQUIP_PER_PAGE}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            equipamiento = data.get('equipmentkits', [])
            total = data.get('total', 0)
    except requests.RequestException:
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
    try:
        resp = requests.put(f"{BACKEND_URL}/equipmentkit/{kit_id}", json=payload, timeout=5)
        if resp.status_code == 200:
            flash("Equipamiento actualizado.", "success")
        else:
            flash("No se pudo actualizar el equipamiento.", "warning")
    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "warning")
    return redirect(url_for('admin_equipamiento'))

@app.route('/admin_equipamiento/eliminar/<int:kit_id>', methods=['POST'])
def eliminar_equipamiento(kit_id):
    try:
        requests.delete(f"{BACKEND_URL}/equipmentkit/{kit_id}", timeout=5)
        flash("Equipamiento eliminado.", "success")
    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "warning")
    return redirect(url_for('admin_equipamiento'))

@app.route('/admin_equipamiento/info/<int:kit_id>', methods=['GET', 'POST'])
def admin_equipamiento_info(kit_id):
    if request.method == "POST":
        link = request.form.get("purchase_link")
        kit = _fetch_equipment_kit(kit_id)
        if not kit:
            flash("Equipamiento no encontrado.", "warning")
            return redirect(url_for('admin_equipamiento'))
        payload = {
            "name": kit["name"],
            "brand": kit["brand"],
            "price": kit["price"],
            "quantity": kit["quantity"],
            "purchase_link": link,
        }
        try:
            resp = requests.put(f"{BACKEND_URL}/equipmentkit/{kit_id}", json=payload, timeout=5)
            if resp.status_code == 200:
                flash("Link de compra actualizado.", "success")
            else:
                flash("No se pudo actualizar el link.", "warning")
        except requests.RequestException:
            flash("No se pudo conectar con el servidor.", "warning")
        return redirect(url_for('admin_equipamiento_info', kit_id=kit_id))

    kit = _fetch_equipment_kit(kit_id)
    if not kit:
        flash("Equipamiento no encontrado.", "warning")
        return redirect(url_for('admin_equipamiento'))
    return render_template('admin_equipamiento_info.html', kit=kit,
                           usuario=session.get('usuario'))

def _fetch_equipment_kit(kit_id):
    try:
        resp = requests.get(f"{BACKEND_URL}/equipmentkit/{kit_id}", timeout=5)
        if resp.status_code == 200:
            return resp.json().get('equipmentkit')
    except requests.RequestException:
        pass
    return None
# 20. Ruta para la página de Equipamientos - Chalecos
@app.route('/equipamientoinfo/chaleco')
def equipamiento_chaleco():
    return render_template('equipamiento_chaleco.html', usuario=session.get('usuario'))
# 21. Ruta para la página de Equipamientos - Casco
@app.route('/equipamientoinfo/casco')
def equipamiento_casco():
    return render_template('equipamiento_casco.html', usuario=session.get('usuario'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/mensaje_logout")
def mensaje_logout():
    session.clear()
    return render_template("mensaje_logout.html")

# Rutas para ver el detalle de cada servicio en particular
@app.route('/servicios/buffet')
def servicio_buffet():
    return render_template('servicio_buffet.html')

@app.route('/servicios/estacionamiento')
def servicio_estacionamiento():
    return render_template('servicio_estacionamiento.html')

@app.route('/servicios/almacenamiento')
def servicio_almacenamiento():
    return render_template('servicio_almacenamiento.html')

# 22. Ruta para la página Sobre Nosotros
@app.route("/nosotros")
def nosotros():
    return render_template('nosotros.html', usuario=session.get('usuario'))


# 23. Ruta para la página de Competitivo / Eventos
@app.route("/competitivo")
def competitivo():
    return render_template("competitivo.html", usuario=session.get('usuario'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
