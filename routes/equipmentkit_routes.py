from flask import Blueprint
from controllers.equipmentkit_controllers import *


equipmentkit_bp = Blueprint('equipmentkit', __name__)


equipmentkit_bp.route('/', methods=['GET'])(listar_kit_equipamientos)
