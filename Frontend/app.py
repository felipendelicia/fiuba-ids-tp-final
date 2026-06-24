from flask import Flask, session
from routes.public import register as register_public
from routes.auth import register as register_auth
from routes.profile import register as register_profile
from routes.reservations import register as register_reservations
from routes.admin import register as register_admin

app = Flask(__name__)
app.secret_key = 'kinetix_clave_super_secreta_para_las_sesiones'


@app.context_processor
def inject_usuario():
    return dict(usuario=session.get("usuario"))

register_public(app)
register_auth(app)
register_profile(app)
register_reservations(app)
register_admin(app)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)