from flask import Blueprint
from controllers.competitivo_controllers import *

competitivo_bp = Blueprint('competitivo', __name__)

competitivo_bp.route('/', methods=['GET'])(listar_eventos)
competitivo_bp.route('/', methods=['POST'])(crear_evento)
competitivo_bp.route('/<int:id>', methods=['GET'])(obtener_evento)
competitivo_bp.route('/<int:id>', methods=['PUT'])(reemplazar_evento)
competitivo_bp.route('/<int:id>', methods=['DELETE'])(eliminar_evento)