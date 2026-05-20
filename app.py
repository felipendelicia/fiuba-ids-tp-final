from flask import Flask, render_template

app = Flask(__name__)

# 1. Ruta para la página principal (Inicio)
@app.route("/")
def index():
    return render_template('indexreservas.html')

# 2. Ruta para la página de reseñas
@app.route("/reseñas")
def reseñas():
    return render_template('adminresenas.html')
# 3. Ruta para la página de administración de reservas
@app.route("/admin-reservas")
def admin_reservas():
    return render_template('adminreservas.html')
@app.route("/sala-privada")
def sala_privada():
    return render_template('salaprivada.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/password')
def password():
  return render_template('password.html')

@app.route('/dashboard')
def dasboard():
  return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)