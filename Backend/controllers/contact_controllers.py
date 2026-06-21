from flask import jsonify, request
from services.contact_services import crear_mensaje, listar_mensajes, marcar_leido


def enviar_mensaje():
    data = request.json or {}
    user_name = data.get('user_name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()
    if not all([user_name, email, message]):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400
    crear_mensaje(user_name, email, message)
    return jsonify({'message': 'Mensaje enviado'}), 201


def ver_mensajes():
    mensajes = listar_mensajes()
    return jsonify(mensajes), 200


def leer_mensaje(msg_id):
    marcar_leido(msg_id)
    return jsonify({'message': 'ok'}), 200