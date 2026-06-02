from flask import Flask, flash, render_template, request, redirect, url_for, session
from  datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'kinetix_clave_super_secreta_para_las_sesiones'
app.permanent_session_lifetime = timedelta(days=7)  

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
                "succes",
            )
            return render_template("index.html")
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

    return render_template("envia_reseña.html")


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
    nombre_usuario = usuario["user_name"]
    if not usuario:
        return redirect(url_for('login_sesion'))
    return render_template('reseñas.html', usuario=usuario, nombre_usuario=nombre_usuario)


@app.route("/perfil/reseñas/ver-reseñas")
def ver_reseñas():

    return render_template("ver_reseñas.html", reseñas=reseñas_globales, usuario=session.get("usuario"), nombre_usuario=session.get("user_name")    )

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

# 9. Ruta para la página de Sala Privada
@app.route("/sala-privada")
def sala_privada():
    return render_template("salaprivada.html")


# 10. Ruta para la página de Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    fecha_actual = datetime.today()
    dia_actual = fecha_actual.day

    dias_mes_actual = [
        31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
    ]

    response = {
        "Dashboard": [
            {
                "id_reserva": 1,
                "user_name": "Pepe Ramirez",
                "dni_usuario": "11534484",
                "price": 30000,
                "start_time": "2025-05-12 10:30:00",
                "end_time": "2025-05-12 12:30:00",
            },
            {
                "id_reserva": 2,
                "user_name": "Juan Luis",
                "dni_usuario": "11534484",
                "price": 1200,
                "start_time": "2025-05-12 13:30:00",
                "end_time": "2025-05-12 14:30:00",
            }
        ]
    }
    lista_reservas_ocu = response["Dashboard"]
    max_reservas = 15
    cant_disponible = max_reservas - len(response["Dashboard"])
    reservas_dis = {"Dashboard_dispo": []}
    for i in range(cant_disponible):
        reservas_dis["Dashboard_dispo"].append(
            {
                "id_reserva": "-",
                "user_name": "-",
                "dni_usuario": "-",
                "price": "-",
                "start_time": "-",
                "end_time": "-",
            }
        )

    horas_reservadas = {
        "cs": 0, "so": 0, "nd": 0, "od": 0, "tc": 0, "qs": 0, "do": 0, "dv": 0
    }
    for reserva in response["Dashboard"]:
        dt = datetime.strptime(reserva["start_time"], "%Y-%m-%d %H:%M:%S")
        hora = dt.hour

        if 5 <= hora < 7:
            horas_reservadas["cs"] += 1
        elif 7 <= hora < 9:
            horas_reservadas["so"] += 1
        elif 9 <= hora < 11:
            horas_reservadas["nd"] += 1
        elif 11 <= hora < 13:
            horas_reservadas["od"] += 1
        elif 13 <= hora < 15:
            horas_reservadas["tc"] += 1
        elif 15 <= hora < 17:
            horas_reservadas["qs"] += 1
        elif 17 <= hora < 19:
            horas_reservadas["do"] += 1
        elif 19 <= hora < 21:
            horas_reservadas["dv"] += 1
    cant_reserva = {"dia": 12, "semana": 80,"mes":320}
    return render_template('admin_dashboard.html', cantidad=cant_reserva, mes_actual=dias_mes_actual, dia_actual=dia_actual, data_ocu=lista_reservas_ocu, data_dis=reservas_dis["Dashboard_dispo"], frec_reservas=horas_reservadas, usuario=session.get('usuario'))

# 13. Ruta para la página de Sala Privada
@app.route("/lobby-privada")
def lobby_privada():
    usuario = session.get('usuario')
    if not usuario:
        flash("Debes iniciar sesión para acceder a la sala privada.", "warning")
        return redirect(url_for('login_sesion'))
    return render_template('lobby_privada.html', usuario=session.get('usuario'))

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
        return render_template('admin_equipamiento.html', equipamiento=equipamiento_db)
    return render_template('admin_equipamiento.html', equipamiento=equipamiento_db)
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

@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)