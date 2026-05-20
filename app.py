import os

from dotenv import load_dotenv
from flask import Flask


from routes.account_routes import account_bp
from routes.authentication_routes import authentication_bp
from routes.gamemodes_routes import gamemodes_bp
from routes.reviews_routes import reviews_bp
from routes.reservations_routes import reservations_bp
from routes.dashboard_routes import dashboard_bp
from routes.maps_routes import maps_bp
from routes.equipmentkit_routes import equipmentkit_bp



load_dotenv()

app = Flask(__name__)

app.register_blueprint(account_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(gamemodes_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(reservations_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(maps_bp)
app.register_blueprint(equipmentkit_bp)

# Para modificar en el desarrollo:
if __name__ == '__main__':
    if os.getenv('ENV') == 'dev':
        app.run(debug= True, port=os.getenv('FLASK_PORT'))
    else:
        app.run(debug= False, host='0.0.0.0', port=os.getenv('FLASK_PORT'))



