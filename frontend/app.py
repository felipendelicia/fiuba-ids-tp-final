import sys, os
from flask import Flask, flash, render_template, request, redirect, url_for, session
from datetime import date, datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'dev'))

# Import dashboard services with fallback if DB is unavailable
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

usuario_admin = {"id": 1, "name" : "Milhouse", "dni" : "13451325", "user_name" : "Dominador", "email": "Milhouse@gmail.com", "phone" : "135454754", "password": "Bart", "gender" : "Masculino", "is_admin" : True}
usuario_existente = { "id": 2, "name" : "Martin", "dni" :"13451325", "user_name" : "El indestructible", "email" : "martin@gmail.com", "gender" : "-", "phone" : "135454754", "password" : "martin", "is_admin" : False}
usuario_nuevo = {"id":3 , "name" : "", "dni" :"", "user_name" : "", "email" : "", "gender" : "", "phone" : "", "password" : "", "is_admin" : "False"}

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

        if email == usuario_existente["email"] and password == usuario_existente["password"]:
            if recuerdame:
                session.permanent = True
            session['usuario'] = usuario_existente
            return redirect(url_for('perfil'))

        elif email == usuario_nuevo["email"] and password == usuario_nuevo["password"]:
            if recuerdame:
                session.permanent = True
            session['usuario'] = usuario_nuevo
            return redirect(url_for('perfil'))

        elif email == usuario_admin["email"] and password == usuario_admin["password"]:
            if recuerdame:
                session.permanent = True
            session['usuario'] = usuario_admin
            return redirect(url_for('perfil'))
        else:
            flash("Usuario o contraseña inválidos.", "warning")

    return render_template('login_sesion.html')

# 3. Ruta para la página de Registrar Nuevo Usuario
@app.route('/login/registro', methods=['GET', 'POST'])
def login_registro():
    if (request.method == 'POST'):
        name = request.form.get('name')
        dni = request.form.get('dni')
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        password = request.form.get('password')
        usuario_nuevo['name'] = name
        usuario_nuevo['dni'] = dni
        usuario_nuevo['user_name'] = user_name
        usuario_nuevo['email'] = email
        usuario_nuevo['gender'] = gender
        usuario_nuevo['phone'] = phone
        usuario_nuevo['password'] = password
        return redirect(url_for('login_sesion'))
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
@app.route('/campos/informacion')
def info_mapa():
    return render_template('vista_mapa.html')

# 6. Ruta para la página de de perfil del usuario
@app.route('/perfil')
def perfil(): 
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('login_sesion'))
    return render_template('perfil.html', usuario=usuario) 

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
    return render_template('admin_creacionsalapublica.html')

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


# --- SISTEMA DE RESEÑAS CON ESTRELLAS DINÁMICAS Y RESPUESTAS DEL ADMIN ---
reseñas_globales = [
    {
        "id": 1,
        "usuario": "Martin",
        "titulo": "¡Excelente servicio y jugabilidad!",
        "mapa": "bunker subterráneo alpha",
        "comentario": "Las réplicas andan bárbaro y los chalecos tácticos marcan perfecto los impactos en tiempo real. Estaría bueno que sumen más variedad de snacks en el entretiempo.",
        "puntuacion": 5,
        "respuestas": [],
    }
]

@app.route("/guardar-reseña", methods=["POST"])
def guardar_reseña():
    usuario = session.get('usuario')
    if not usuario:
        flash("Debes iniciar sesión para enviar una reseña.", "warning")
        return redirect(url_for('login_sesion'))
    
    nombre_usuario = usuario.get("user_name", "Usuario Anónimo")
    titulo = request.form.get("titulo")
    mapa = request.form.get("mapa")
    comentario = request.form.get("comentario")
    puntuacion = request.form.get("puntuacion")

    if comentario and puntuacion:
        nueva_reseña = {
            "id": len(reseñas_globales) + 1,
            "usuario": nombre_usuario,
            "titulo": titulo if titulo else "Reseña General",
            "mapa": mapa if mapa else "General",
            "comentario": comentario,
            "puntuacion": int(puntuacion),
            "respuestas": [],
        }
        reseñas_globales.append(nueva_reseña)

    return render_template("mensaje_envia_resenia.html", usuario=session.get ('usuario'))


# SOLUCIONADO: Se eliminó la eñe de la URL dinámica para prevenir el ValueError de Werkzeug
@app.route("/adminreseñas/responder/<int:resena_id>", methods=["POST"])
def responder_reseña(resena_id):
    texto_respuesta = request.form.get("respuesta_admin")

    if texto_respuesta:
        for r in reseñas_globales:
            if r["id"] == resena_id:
                nueva_respuesta = {
                    "autor": "Soporte Kinetix (Admin)",
                    "texto": texto_respuesta,
                }
                r["respuestas"].append(nueva_respuesta)
                break

    return redirect(url_for("admin_reseñas"))


@app.route("/perfil/reseñas")
def reseñas():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('login_sesion'))
    nombre_usuario = usuario["user_name"]
    return render_template('reseñas.html', usuario=usuario, nombre_usuario=nombre_usuario)


@app.route("/perfil/reseñas/ver-reseñas")
def ver_reseñas():
    usuario = session.get("usuario")
    nombre_usuario = usuario["user_name"] if usuario else None
    return render_template("ver_reseñas.html", reseñas=reseñas_globales, usuario=usuario, nombre_usuario=nombre_usuario)

@app.route("/admin_panel")
def admin_panel():
    return render_template("admin_panel.html", usuario=session.get("usuario"))

@app.route("/admin_reseñas")
def admin_reseñas():
    return render_template("admin_reseñas.html", reseñas=reseñas_globales, usuario=session.get("usuario"))

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
# 13. Ruta para la página de Sala Privada
@app.route("/lobby-privada")
def lobby_privada():
    usuario = session.get('usuario')
    if not usuario:
        flash("Debes iniciar sesión para acceder a la sala privada.", "warning")
        return redirect(url_for('login_sesion'))
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
                           anio=hoy.year)

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
    equipamiento_db = [
        {"id": 1, "tipo": "Pelota de Fútbol 5", "cantidad": 10},
        {"id": 2, "tipo": "Pecheras (Set x 5)", "cantidad": 8},
    ]
    if request.method == "POST":
        tipo = request.form.get("tipo")
        cantidad = int(request.form.get("cantidad"))
        nuevo_id = len(equipamiento_db) + 1
        equipamiento_db.append({"id": nuevo_id, "tipo": tipo, "cantidad": cantidad})
        return render_template('admin_equipamiento.html', equipamiento=equipamiento_db, usuario=session.get('usuario'))
    return render_template('admin_equipamiento.html', equipamiento=equipamiento_db, usuario=session.get('usuario'))
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

# 22. Ruta para la página de Competitivo / Eventos
@app.route("/competitivo")
def competitivo():
    return render_template("competitivo.html", usuario=session.get('usuario'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)