from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#1. Ruta para la página de Inicio
@app.route("/")
def index():
    return render_template('index.html')

# 2. Ruta para la página de Iniciar Sesion
@app.route("/login")
def login():
    return render_template('login.html')

# 3. Ruta para la página de Registrar Nuevo Usuario
@app.route('/register')
def register():
  return render_template('register.html')

# 4. Ruta para la pagína de Recuperación Contraseña de Usuario
@app.route('/password')
def password():
  return render_template('password.html')

# 5. Ruta para la página de Campos de Juegos
@app.route("/campos")
def campos():
    return render_template('campos.html')

# 6. Ruta para la página Reservas de Campos
@app.route("/reservas")
def reservas():
    return render_template('reservas.html')

# 7. Ruta para la página de Reseñas
@app.route("/reseñas")
def reseñas():
    return render_template('adminresenas.html')

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

# 12. Ruta para la página de Reserva de Sala Pública
@app.route("/sala-publica")
def sala_publica():
    return render_template('salaspublicas.html')

# 13. Ruta para la página de Servicios
@app.route('/servicios')
def servicios():
    servicios_db = [
        {"id": 1, "nombre": "Bufet / Bar", "descripcion": "Venta de bebidas y comidas post-partido."},
        {"id": 2, "nombre": "Estacionamiento", "descripcion": "Predio cerrado con seguridad para autos y motos."}
    ]
    return render_template('servicios.html', servicios=servicios_db)

# 14. Ruta para la página de Contacto
@app.route('/contacto', methods=['GET', 'POST'])
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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)