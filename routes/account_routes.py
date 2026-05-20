from flask import Blueprint
from controllers.account_controllers import *

account_bp = Blueprint('account', __name__)

account_bp.route('/', methods=['GET'])(listar_usuarios)
account_bp.route('/<int: id>', methods=['GET'])(obtener_cuenta)
account_bp.route('/<int: id>', methods=['PATCH'])(actualizar_usuario)
account_bp.route('/<int: id>/reservations', methods=['GET'])(listar_reservas)
account_bp.route('/<int: id>/toggle_status', methods=['PATCH'])(actualizar_estado_usuario)
account_bp.route('/<int: id>/gender', methods=['PATCH'])(actualizar_genero_usuario)
account_bp.route('/<int: id>/password', methods=['PATCH'])(actualizar_password_usuario)

