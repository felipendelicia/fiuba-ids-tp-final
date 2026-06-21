from flask import Blueprint
from controllers.equipmentkit_controllers import *


equipmentkit_bp = Blueprint('equipmentkit', __name__)


equipmentkit_bp.route('/', methods=['GET'])(listar_kit_equipamientos)
equipmentkit_bp.route('/', methods=['POST'])(crear_kit_equipamiento)
equipmentkit_bp.route('/<int:id>', methods=['GET'])(obtener_kit_equipamiento)
equipmentkit_bp.route('/<int:id>', methods=['PUT'])(reemplazar_kit_equipamiento)
equipmentkit_bp.route('/<int:id>', methods=['DELETE'])(eliminar_kit_equipamiento)
