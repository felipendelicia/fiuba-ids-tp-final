import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException


from routes.account_routes import account_bp
from routes.authentication_routes import authentication_bp
from routes.gamemodes_routes import gamemodes_bp
from routes.reviews_routes import reviews_bp
from routes.reservations_routes import reservations_bp
from routes.dashboard_routes import dashboard_bp
from routes.maps_routes import maps_bp
from routes.equipmentkit_routes import equipmentkit_bp
from routes.competitivo_routes import competitivo_bp
from routes.nosotros_routes import nosotros_bp
from routes.contact_routes import contact_bp
from routes.service_routes import service_bp
from routes.salas_routes import salas_bp



load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or 'dev-secret-change-me'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)

app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(authentication_bp, url_prefix='/authentication')
app.register_blueprint(gamemodes_bp, url_prefix='/gamemodes')
app.register_blueprint(reviews_bp, url_prefix='/reviews')
app.register_blueprint(reservations_bp, url_prefix='/reservations')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(maps_bp, url_prefix='/maps')
app.register_blueprint(equipmentkit_bp, url_prefix='/equipmentkit')
app.register_blueprint(competitivo_bp, url_prefix='/competitivo')
app.register_blueprint(nosotros_bp, url_prefix='/nosotros')
app.register_blueprint(contact_bp, url_prefix='/contacto')
app.register_blueprint(service_bp, url_prefix='/services')
app.register_blueprint(salas_bp, url_prefix='/salas')


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    return jsonify({'errors': [{
        'code': error.code,
        'message': error.description,
        'level': 'error',
    }]}), error.code


# Para modificar en el desarrollo:
if __name__ == '__main__':
    if os.getenv('ENV') == 'dev':
        app.run(debug= True, port=os.getenv('FLASK_PORT'))
    else:
        app.run(debug= False, host='0.0.0.0', port=os.getenv('FLASK_PORT'))



