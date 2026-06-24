import json
from flask import jsonify
from services.nosotros_services import obtener_info, listar_cards


def nosotros():
    info = obtener_info()
    if info and info.get('paragraphs'):
        try:
            info['paragraphs'] = json.loads(info['paragraphs'])
        except (json.JSONDecodeError, TypeError):
            info['paragraphs'] = []
    cards = listar_cards()
    return jsonify({
        'info': info,
        'cards': cards,
    }), 200