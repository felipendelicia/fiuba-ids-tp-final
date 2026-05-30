from flask import jsonify, request
from controllers.equipmentkit_controllers import *


def servicio_obtener_todos():
    try:
        lista = db_seleccionar_todos()
        return jsonify(lista), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def servicio_obtener_por_id(id_equipment):
    try:
        equipamiento = db_seleccionar_por_id(id_equipment)
        if equipamiento:
            return jsonify(equipamiento), 200
        return jsonify({"mensaje": "Equipamiento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def servicio_crear_nuevo():
    try:
        datos = request.get_json()
        name, tipo, price, stock = datos.get('name'), datos.get('type'), datos.get('price'), datos.get('stock')

        if not name or not tipo or price is None or stock is None:
            return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

        nuevo_id = db_insertar_equipamiento(name, tipo, price, stock)
        return jsonify({"mensaje": "Creado con éxito", "id": nuevo_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def servicio_actualizar(id_equipment):
    try:
        datos = request.get_json()
        filas = db_actualizar_equipamiento(id_equipment, datos.get('name'), datos.get('type'), datos.get('price'),
                                           datos.get('stock'))
        if filas > 0:
            return jsonify({"mensaje": "Actualizado correctamente"}), 200
        return jsonify({"mensaje": "No encontrado o sin cambios"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def servicio_eliminar(id_equipment):
    try:
        filas = db_eliminar_equipamiento(id_equipment)
        if filas > 0:
            return jsonify({"mensaje": "Eliminado correctamente"}), 200
        return jsonify({"mensaje": "No encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500