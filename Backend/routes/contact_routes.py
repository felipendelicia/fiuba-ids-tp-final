from flask import Blueprint
from controllers.contact_controllers import enviar_mensaje, ver_mensajes, leer_mensaje

contact_bp = Blueprint('contact_bp', __name__)

contact_bp.route('/', methods=['POST'])(enviar_mensaje)
contact_bp.route('/', methods=['GET'])(ver_mensajes)
contact_bp.route('/<int:msg_id>/leer', methods=['POST'])(leer_mensaje)