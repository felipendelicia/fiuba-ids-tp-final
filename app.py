from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#1. Ruta para la página de Inicio
@app.route("/")
def index():
    return render_template('index.html')

# 2. Ruta para la página de Iniciar Sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    # usuario que fue enviado de la api
    usuario = {
        "email": "piter@gmail.com",
        "password": "piter123"
    }
    if (request.method == 'POST'):
        email = request.form.get("email")
        password = request.form.get("password")
        recuerdame = request.form.get("recuerdame")

        if(password == usuario["password"] and email == usuario["email"]):
            # falta implementar el recuerdame ....
          return render_template('perfil.html')
        else:
            print('Necesitas iniciar sesion primero')

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
        print(nuevo_usuario)
        return render_template('perfil.html', usuario = nuevo_usuario)
    return render_template('register.html')

# 4. Ruta para la pagína de Recuperación Contraseña de Usuario
@app.route('/password', methods=['GET', 'POST'])
def password():
    #email que del usuario para enviarle instruccuiones de cambiar contraseña
    email_user = "piter@gmail.com"
    if (request.method == 'POST'):
        email = request.form.get('email')
        if (email == email_user):
            print("se envio instrucciones para recueperar la contraseña")
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

# 7. Ruta para la página de Reseñas
@app.route("/perfil/reseñas")
def reseñas():
    return render_template('reseñas.html')

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
def dasboard():
  return render_template('dashboard.html')

# 11. Ruta para la página de Lobby para Salas Públicas
@app.route("/lobby-publicas")
def lobby_publicas():
    return render_template('lobbypublicas.html')

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
# Error de pagina
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)