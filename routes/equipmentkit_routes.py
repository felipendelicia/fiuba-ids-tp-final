from flask import Blueprint
from services.equipmentkit_services import *

equipmentkit_bp = Blueprint('equipmentkit_bp', __name__)

@equipmentkit_bp.route('/', methods=['GET'])
def obtener_equipamientos():
    return servicio_obtener_todos()

@equipmentkit_bp.route('/', methods=['POST'])
def crear_equipamiento():
    return servicio_crear_nuevo()

@equipmentkit_bp.route('/<int:id_equipment>', methods=['GET'])
def obtener_equipamiento(id_equipment):
    return servicio_obtener_por_id(id_equipment)

@equipmentkit_bp.route('/<int:id_equipment>', methods=['PUT'])
def actualizar_equipamiento(id_equipment):
    return servicio_actualizar(id_equipment)

@equipmentkit_bp.route('/<int:id_equipment>', methods=['DELETE'])
def eliminar_equipamiento(id_equipment):
    return servicio_eliminar(id_equipment)