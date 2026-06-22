from flask import jsonify


def build_paginated_response(items_key, items, total, links, item_builder=None):
    if item_builder:
        items = [item_builder(item) for item in items]
    return jsonify({
        items_key: items,
        'total': total,
        '_links': links
    }), 200


def build_created_response(message):
    return jsonify({'message': message}), 201


def build_updated_response(message):
    return jsonify({'message': message}), 200
