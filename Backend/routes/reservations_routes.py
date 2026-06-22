from flask import Blueprint
from controllers.reservations_controllers import listar_reservas, join_sala, actualizar_reserva

reservations_bp = Blueprint('reservations', __name__)

reservations_bp.route('/', methods=['GET'])(listar_reservas)
reservations_bp.route('/register/<int:sala_id>', methods=['POST'])(join_sala)
reservations_bp.route('/<int:id>', methods=['PATCH'])(actualizar_reserva)
