from flask import jsonify, request
from dtos.errors import abort
from services.competitivo_services import (
    listar_eventos as service_listar,
    obtener_evento as service_obtener,
    crear_evento as service_crear,
    reemplazar_evento as service_reemplazar,
    eliminar_evento as service_eliminar,
)


def listar_eventos():
    try:
        offset = int(request.args.get('_offset', 0))
        limit = int(request.args.get('_limit', 100))
    except ValueError:
        abort(400, '_offset y _limit deben ser enteros')
    eventos, total = service_listar(offset, limit)
    return jsonify({'events': eventos, 'total': total}), 200


def obtener_evento(id):
    evento = service_obtener(id)
    return jsonify({'event': evento}), 200


def crear_evento():
    data = request.get_json()
    if not data or not data.get('title'):
        abort(400, 'Campo requerido: title')
    service_crear(
        title=data['title'].strip(),
        description=data.get('description'),
        image_url=data.get('image_url'),
        badge=data.get('badge'),
        event_date=data.get('event_date'),
        event_time=data.get('event_time'),
    )
    return jsonify({'message': 'Evento creado exitosamente'}), 201


def reemplazar_evento(id):
    data = request.get_json()
    if not data or not data.get('title'):
        abort(400, 'Campo requerido: title')
    service_reemplazar(
        id,
        title=data['title'].strip(),
        description=data.get('description'),
        image_url=data.get('image_url'),
        badge=data.get('badge'),
        event_date=data.get('event_date'),
        event_time=data.get('event_time'),
    )
    return jsonify({'message': 'Evento actualizado exitosamente'}), 200


def eliminar_evento(id):
    service_eliminar(id)
    return jsonify({'message': 'Evento eliminado exitosamente'}), 200