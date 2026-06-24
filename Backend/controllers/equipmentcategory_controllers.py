from flask import jsonify
from services.equipmentcategory_services import listar_categorias as service_listar


def listar_categorias():
    categorias = service_listar()
    return jsonify({'categories': categorias}), 200