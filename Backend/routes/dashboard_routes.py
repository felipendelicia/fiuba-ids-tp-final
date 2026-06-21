from flask import Blueprint
from controllers.dashboard_controllers import *


dashboard_bp = Blueprint('dashboard', __name__)

dashboard_bp.route('/disponibility/', methods=['GET'])(listar_periodo_reservas)
dashboard_bp.route('/data/', methods=['GET'])(api_dashboard_data)


