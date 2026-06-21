from flask import Blueprint
from controllers.nosotros_controllers import nosotros

nosotros_bp = Blueprint('nosotros_bp', __name__)

nosotros_bp.route('/', methods=['GET'])(nosotros)