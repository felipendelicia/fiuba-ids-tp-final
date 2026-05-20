from flask import Blueprint
from controllers.authentication_controllers import *

authentication_bp = Blueprint('authentication', __name__)

authentication_bp.route('/login', methods=['POST'])(login_usuario)
authentication_bp.route('/register', methods=['POST'])(registrar_usuario)
