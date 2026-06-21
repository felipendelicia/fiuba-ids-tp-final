from flask import Blueprint
from Backend.controllers.maps_controllers import *

maps_bp = Blueprint('maps', __name__)

maps_bp.route('/disponibility', methods=['GET'])(listar_mapas)
