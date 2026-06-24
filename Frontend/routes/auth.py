from flask import flash, render_template, request, redirect, url_for, session
from helpers import _api_post, _api_get_usuario


def register(app):

    @app.route('/login/sesion', methods=['GET', 'POST'])
    def login_sesion():
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")
            recuerdame = request.form.get("recuerdame")

            resp = _api_post("/authentication/login", data={"email": email, "password": password})
            if resp is None:
                flash("No se pudo conectar con el servidor.", "warning")
                return render_template('login_sesion.html')

            if resp.status_code == 200:
                data = resp.json()
                usuario = _api_get_usuario(data["user_id"])
                if usuario:
                    usuario["token"] = data.get("token")
                    if recuerdame:
                        session.permanent = True
                    session['usuario'] = usuario
                    return redirect(url_for('perfil'))
                flash("No se pudo obtener el perfil del usuario.", "warning")
            else:
                flash("Usuario o contraseña invalidos.", "warning")

        return render_template('login_sesion.html')

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
            resp = _api_post("/authentication/register", data=payload)
            if resp is None:
                flash("No se pudo conectar con el servidor.", "warning")
                return render_template('login_registro.html')

            if resp.status_code == 201:
                flash("Registro exitoso. Inicia sesion.", "success")
                return redirect(url_for('login_sesion'))

            msg = "No se pudo completar el registro."
            try:
                msg = resp.json()["errors"][0]["message"]
            except Exception:
                pass
            flash(msg, "warning")
        return render_template('login_registro.html')

    @app.route('/login/contrasenia', methods=['GET', 'POST'])
    def login_contrasenia():
        if request.method == "POST":
            flash("Hemos enviado un correo con instrucciones de recuperacion. Revisa tu bandeja de entrada y la carpeta de spam", "success")
            return redirect(url_for('index'))
        return render_template('login_contrasenia.html')

    @app.route("/mensaje_logout")
    def mensaje_logout():
        session.clear()
        return render_template("mensaje_logout.html")
