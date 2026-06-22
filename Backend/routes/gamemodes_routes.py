from flask import Blueprint
from controllers.gamemodes_controllers import *

gamemodes_bp = Blueprint('gamemodes', __name__)

gamemodes_bp.route('/', methods=['GET'])(listar_game_modes)
gamemodes_bp.route('/', methods=['POST'])(crear_game_mode)
gamemodes_bp.route('/<int:id>', methods=['PUT'])(reemplazar_game_mode)
gamemodes_bp.route('/<int:id>', methods=['DELETE'])(eliminar_game_mode)
gamemodes_bp.route('/<int:id>/maps', methods=['PUT'])(reemplazar_mapas_de_modo)





