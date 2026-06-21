import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException


from Backend.routes.account_routes import account_bp
from Backend.routes.authentication_routes import authentication_bp
from Backend.routes.gamemodes_routes import gamemodes_bp
from Backend.routes.reviews_routes import reviews_bp
from Backend.routes.reservations_routes import reservations_bp
from Backend.routes.dashboard_routes import dashboard_bp
from Backend.routes.maps_routes import maps_bp
from Backend.routes.equipmentkit_routes import equipmentkit_bp



load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(authentication_bp, url_prefix='/authentication')
app.register_blueprint(gamemodes_bp, url_prefix='/gamemodes')
app.register_blueprint(reviews_bp, url_prefix='/reviews')
app.register_blueprint(reservations_bp, url_prefix='/reservations')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(maps_bp, url_prefix='/maps')
app.register_blueprint(equipmentkit_bp, url_prefix='/equipmentkit')


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



