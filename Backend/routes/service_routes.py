from flask import Blueprint
from controllers.service_controllers import (
    get_services, get_service, create_service, update_service, delete_service,
)

service_bp = Blueprint('service_bp', __name__)

service_bp.route('/', methods=['GET'])(get_services)
service_bp.route('/', methods=['POST'])(create_service)
service_bp.route('/<int:service_id>', methods=['GET'])(get_service)
service_bp.route('/<int:service_id>', methods=['PUT'])(update_service)
service_bp.route('/<int:service_id>', methods=['DELETE'])(delete_service)