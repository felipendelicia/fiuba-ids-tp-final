from flask import Blueprint
from controllers.equipmentkit_controllers import *
from controllers.equipmentcategory_controllers import listar_categorias


equipmentkit_bp = Blueprint('equipmentkit', __name__)


equipmentkit_bp.route('/', methods=['GET'])(listar_kit_equipamientos)
equipmentkit_bp.route('/', methods=['POST'])(crear_kit_equipamiento)
equipmentkit_bp.route('/categories', methods=['GET'])(listar_categorias)
equipmentkit_bp.route('/<int:id>', methods=['GET'])(obtener_kit_equipamiento)
equipmentkit_bp.route('/<int:id>', methods=['DELETE'])(eliminar_kit_equipamiento)
