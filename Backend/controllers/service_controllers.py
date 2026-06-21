from flask import jsonify, request
from services.service_services import (
    listar_servicios, obtener_servicio,
    crear_servicio, actualizar_servicio, eliminar_servicio,
)


def get_services():
    servicios = listar_servicios()
    return jsonify({"services": servicios}), 200


def get_service(service_id):
    s = obtener_servicio(service_id)
    if not s:
        return jsonify({"error": "Servicio no encontrado"}), 404
    return jsonify({"service": s}), 200


def create_service():
    data = request.json or {}
    crear_servicio(data)
    return jsonify({"message": "Servicio creado"}), 201


def update_service(service_id):
    if not obtener_servicio(service_id):
        return jsonify({"error": "Servicio no encontrado"}), 404
    data = request.json or {}
    actualizar_servicio(service_id, data)
    return jsonify({"message": "Servicio actualizado"}), 200


def delete_service(service_id):
    if not obtener_servicio(service_id):
        return jsonify({"error": "Servicio no encontrado"}), 404
    eliminar_servicio(service_id)
    return jsonify({"message": "Servicio eliminado"}), 200