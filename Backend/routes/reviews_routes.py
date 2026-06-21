from flask import Blueprint
from controllers.reviews_controllers import *

reviews_bp = Blueprint('review', __name__)


reviews_bp.route('/', methods=['GET'])(listar_reviews)
reviews_bp.route('/', methods=['POST'])(crear_map_review)
reviews_bp.route('/auth/<int:id>', methods=['PATCH'])(actualizar_review)
