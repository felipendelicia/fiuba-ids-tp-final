from flask import Flask, flash, render_template, request, redirect, url_for
from  datetime import datetime

app = Flask(__name__)
app.secret_key = "mi_clave_super_secreta_123"

# 1. Ruta para la página de Inicio
@app.route("/")
def index():
    return render_template('index.html')

# 2. Ruta para la página de Iniciar Sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    # usuario que fue enviado de la api
    usuario = {
        "name" : "Martin",
        "dni" :"13451325",
        "user_name" : "El indestructible",
        "email" : "martin@gmial.com",
        "gender" : "-",
        "phone" : "135454754",
        "password" : "matin123456",
        "es_admin" : "false"
    }

    usuario_admin = {
        "name" : "Milhouse",
        "dni" : "13451325",
        "user_name" : "Dominador",
        "email": "Milhouse@gmail.com",
        "phone" : "135454754",
        "password": "Bart",
        "gender" : "-",
        "es_admin": "true" 
    }
    if (request.method == 'POST'):
        email = request.form.get("email")
        password = request.form.get("password")
        recuerdame = request.form.get("recuerdame")

        if(email == usuario["email"] and password == usuario["password"]):
            return render_template('perfil.html', usuario=usuario)
        elif (email == usuario_admin['email'] and password == usuario_admin['password']):
            return render_template('adminperfil.html', usuario=usuario_admin)
        else:
            flash("Error al iniciar sesión. Verifica tú email y contraseña.", "warning")

    return render_template('login.html')

# 3. Ruta para la página de Registrar Nuevo Usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    # nuevo usuario para enviar a la api
    nuevo_usuario = {}
    if (request.method == 'POST'):
        name = request.form.get('name')
        dni = request.form.get('dni')
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        password = request.form.get('password')

        nuevo_usuario['name'] = name
        nuevo_usuario['dni'] = dni
        nuevo_usuario['user_name'] = user_name
        nuevo_usuario['email'] = email
        nuevo_usuario['gender'] = gender
        nuevo_usuario['phone'] = phone
        nuevo_usuario['password'] = password

        flash("La cuenta ha sido creada exitosamente", "succes")
        return render_template('perfil.html', usuario=nuevo_usuario)
    return render_template('register.html')

# 4. Ruta para la pagína de Recuperación Contraseña de Usuario
@app.route('/password', methods=['GET', 'POST'])
def password():
    #email que del usuario para enviarle instruccuiones de cambiar contraseña
    email_user = "Bruno@gmail.com"
    if (request.method == 'POST'):
        email = request.form.get('email')
        if (email == email_user):
            flash("Hemos enviado un correo con instrucciones de recuperación. Revisa tu bandeja de entrada y la carpeta de spam", "succes")
            return render_template('index.html')
    return render_template('password.html')

# 5. Ruta para la página de Campos de Juegos
@app.route("/notloggedcampos")
def notloggedcampos():
    return render_template('notloggedcampos.html')

@app.route("/perfil/campos")
def campos():
    return render_template('campos.html')

@app.route('/perfil')
def perfil(): 
    return render_template('perfil.html') 

# 6. Ruta para la página Reservas de Campos
@app.route("/reservas")
def reservas():
    return render_template('reservas.html')

@app.route("/perfil/reservaslogged")
def reservaslogged():
    return render_template('reservaslogged.html')

@app.route("/perfil/reservasadmin")
def reservasadmin():
    return render_template('reservasadmin.html')

# --- SISTEMA DE GESTIÓN DE SALAS PÚBLICAS ---
salas_publicas = []
mis_salas_unidas = []  # Almacena los IDs de las salas a las que ya se unió el usuario

@app.route("/perfil/reservasadmin/crearsala", methods=['GET', 'POST'])
def crearsala():
    if request.method == 'POST':
        nueva_partida = {
            "id": request.form.get('id_reserva'),
            "modalidad": request.form.get('modalidad'),
            "escenario": request.form.get('escenario'),
            "fecha": request.form.get('fecha'),
            "hora": request.form.get('hora'),
            "actuales": 0,          
            "maximos": 10,          
            "estado": "[ RESERVA DE ADMIN ]"
        }
        salas_publicas.append(nueva_partida)
        return redirect(url_for('lobby_admin'))
        
    return render_template('creacionsalapublica.html')

@app.route("/perfil/reservasadmin/eliminar/<id_partida>", methods=['POST'])
def eliminar_sala(id_partida):
    global salas_publicas
    salas_publicas = [sala for sala in salas_publicas if sala['id'] != id_partida]
    if id_partida in mis_salas_unidas:
        mis_salas_unidas.remove(id_partida)
    return redirect(url_for('lobby_admin'))

@app.route("/lobby/unirse/<id_partida>", methods=['POST'])
def unirse_sala(id_partida):
    if id_partida not in mis_salas_unidas:
        for sala in salas_publicas:
            if sala['id'] == id_partida and sala['actuales'] < sala['maximos']:
                sala['actuales'] += 1
                mis_salas_unidas.append(id_partida)
                break
    return redirect(url_for('lobby_admin'))

@app.route("/lobby-publico")
def lobby_admin():
    return render_template('lobbypublicas.html', salas=salas_publicas, unidas=mis_salas_unidas)
# ---------------------------------------------

# 7. Ruta para la página de Reseñas
@app.route("/perfil/reseñas")
def reseñas():
    return render_template('reseñas.html')

@app.route("/adminreseñas")
def adminreseñas():
    return render_template('adminreseñas.html')

# 8. Ruta para la página de administración de reservas
@app.route("/admin-reservas")
def admin_reservas():
    return render_template('adminreservas.html')

# 9. Ruta para la página de Sala Privada
@app.route("/sala-privada")
def sala_privada():
    return render_template('salaprivada.html')

# 10. Ruta para la página de Dashboard
@app.route('/dashboard')
def dashboard():
    #fecha del dia actual se utilizara por defecto
    fecha_actual = datetime.today()
    dia_actual = fecha_actual.day
    
    #el mes es --mayo-- entonces los dia del calendario iniciando de lunes a domingo son:,
    dias_mes_actual = [27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    
    #respuesta de listar reservas ocupadas de la api
    response = {"Dashboard": 
        [
            {
                "id_reserva": 1,
                "user_name": "Pepe Ramirez",
                "dni_usuario": "11534484",
                "price": 30000,
                "start_time": "2025-05-12 10:30:00",
                "end_time": "2025-05-12 12:30:00"
            },
            {
                "id_reserva": 2,
                "user_name": "Juan Luis",
                "dni_usuario": "11534484",
                "price": 1200,
                "start_time": "2025-05-12 13:30:00",
                "end_time": "2025-05-12 14:30:00"
            },
            {
                "id_reserva": 3,
                "user_name": "Alfredo",
                "dni_usuario": "11534484",
                "price": 450000,
                "start_time": "2025-05-12 16:30:00",
                "end_time": "2025-05-12 17:30:00"
            } ,
            {
                "id_reserva": 4,
                "user_name": "Javier",
                "dni_usuario": "11534484",
                "price": 450000,
                "start_time": "2025-05-12 16:30:00",
                "end_time": "2025-05-12 17:30:00"
            } ,
            {
                "id_reserva": 5,
                "user_name": "Alvares",
                "dni_usuario": "11534484",
                "price": 450000,
                "start_time": "2025-05-12 16:30:00",
                "end_time": "2025-05-12 17:30:00"
            } ,
            {
                "id_reserva": 6,
                "user_name": "Toreto",
                "dni_usuario": "11534484",
                "price": 450000,
                "start_time": "2025-05-12 07:00:00",
                "end_time": "2025-05-12 12:30:00"
            } 
        ]
    }

    #para rellenar los campos disponibles en la tabla de reservas
    lista_reservas_ocu = response["Dashboard"]

    #calculo y agrego la cantidad restante de reservas disponibles
    max_reservas = 15
    cant_disponible = max_reservas - len(response["Dashboard"])
    reservas_dis = {"Dashboard_dispo": []}
    for i in range(cant_disponible):
        reservas_dis["Dashboard_dispo"].append({ "id_reserva": "-", "user_name": "-","dni_usuario": "-","price": "-","start_time": "-", "end_time": "-"})
    
    #frecuencia de horas de la reserva por dia
    horas_reservadas = {"cs":0 ,"so":0 ,"nd":0 ,"od":0 ,"tc":0 ,"qs":0 ,"do":0,"dv":0}
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
    
    #COSAS POR VER.....
    #deberia existir datos para las reservas por dias, semana, mes, año(lo que va desde el inicio hasta el final del año)
    cant_reserva = {"dia": 12, "semana": 80,"mes":320, "año":2800}
    
    return render_template('dashboard.html', cantidad=cant_reserva, mes_actual=dias_mes_actual, dia_actual=dia_actual, data_ocu=lista_reservas_ocu, data_dis=reservas_dis["Dashboard_dispo"], frec_reservas=horas_reservadas)

# 13. Ruta para la página de Servicios
@app.route('/notloggedservicios')
def notloggedservicios():
    servicios_db = [
        {"id": 1, "nombre": "Bufet / Bar", "descripcion": "Venta de bebidas y comidas post-partido."},
        {"id": 2, "nombre": "Estacionamiento", "descripcion": "Predio cerrado con seguridad para autos y motos."}
    ]
    return render_template('notloggedservicios.html', servicios=servicios_db)

@app.route('/perfil/servicios')
def servicios():
    servicios_db = [
        {"id": 1, "nombre": "Bufet / Bar", "descripcion": "Venta de bebidas y comidas post-partido."},
        {"id": 2, "nombre": "Estacionamiento", "descripcion": "Predio cerrado con seguridad para autos y motos."}
    ]
    return render_template('servicios.html', servicios=servicios_db)

# 14. Ruta para la página de Contacto
@app.route('/notloggedcontacto', methods=['GET', 'POST'])
def notloggedcontacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        return redirect(url_for('contacto'))
    return render_template('notloggedcontacto.html')

@app.route('/perfil/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        return redirect(url_for('contacto'))
    return render_template('contacto.html')

# 15. Ruta para la página de Administrador de Servicios
@app.route('/adminservicios', methods=['GET', 'POST'])
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
        return render_template('adminservicios.html', servicios=servicios_db)
    return render_template('adminservicios.html', servicios=servicios_db)

# 16. Ruta para la página de Equipamientos
@app.route('/notloggedequipamientoinfo')
def notloggedequipamiento_info():
    return render_template('notloggedequipamientoinfo.html')

@app.route('/notloggedequipamientoinfo/notloggedarmasinfo')
def notloggedarmasinfo():
    return render_template('notloggedarmasinfo.html')

@app.route('/perfil/equipamientoinfo')
def equipamiento_info():
    return render_template('equipamientoinfo.html')

@app.route('/perfil/equipamientoinfo/armasinfo')
def armasinfo():
    return render_template('armasinfo.html')

@app.route('/equipamiento', methods=['GET', 'POST'])
def equipamiento():
    equipamiento_db = [
        {"id": 1, "tipo": "Pelota de Fútbol 5", "cantidad": 10},
        {"id": 2, "tipo": "Pecheras (Set x 5)", "cantidad": 8}
    ]
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        cantidad = int(request.form.get('cantidad'))
        nuevo_id = len(equipamiento_db) + 1
        equipamiento_db.append({"id": nuevo_id, "tipo": tipo, "cantidad": cantidad})
        return render_template('equipamiento.html', equipamiento=equipamiento_db)
    return render_template('equipamiento.html', equipamiento=equipamiento_db)

@app.route("/notloggedequipamientoinfo/notloggedchaleco")
def notloggedchaleco():
    return render_template('notloggedchaleco.html')

@app.route("/notloggedequipamientoinfo/notloggedcasco")
def notloggedcasco():
    return render_template('notloggedcasco.html')

@app.route('/perfil/equipamientoinfo/chaleco')
def chaleco():
    return render_template('chaleco.html')

@app.route('/perfil/equipamientoinfo/casco')
def casco():
    return render_template('casco.html')

# Error de pagina
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)