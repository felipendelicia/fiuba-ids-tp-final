from flask import Blueprint
from controllers.reservations_controllers import *

reservations_bp = Blueprint('reservations', __name__)

reservations_bp.route('/', methods=['GET'])(listar_reservas)
reservations_bp.route('/<int:id>', methods=['GET'])(listar_reservas_usuario)
reservations_bp.route('/<int:id>', methods=['POST'])(crear_reserva)
reservations_bp.route('/<int:id>', methods=['PATCH'])(actualizar_reserva)
reservations_bp.route('/register/<int:id>', methods=['POST'])(crear_public_reservation)
