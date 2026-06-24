from flask import Blueprint
from controllers.salas_controllers import listar_salas, crear_sala, actualizar_sala

salas_bp = Blueprint('salas', __name__)

salas_bp.route('/', methods=['GET'])(listar_salas)
salas_bp.route('/', methods=['POST'])(crear_sala)
salas_bp.route('/<int:id>', methods=['PATCH'])(actualizar_sala)
