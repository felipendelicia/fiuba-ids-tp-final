from dtos.errors import abort


def validate_list_equipment(request):
    try:
        offset = int(request.args.get('_offset', 0))
        limit = int(request.args.get('_limit', 10))
    except ValueError:
        abort(400, '_offset y _limit deben ser enteros')
    if offset < 0 or limit < 1:
        abort(400, '_offset >= 0 y _limit >= 1')
    return {'offset': offset, 'limit': limit}


def validate_create_equipment(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    name = data.get('name')
    brand = data.get('brand')
    price = data.get('price')
    quantity = data.get('quantity', 1)
    purchase_link = data.get('purchase_link')
    if not name or price is None:
        abort(400, 'Campos requeridos: name, price')
    return {
        'name': name.strip(),
        'brand': brand.strip() if brand else None,
        'price': float(price),
        'quantity': int(quantity),
        'purchase_link': purchase_link.strip() if purchase_link else None,
    }


validate_replace_equipment = validate_create_equipment


def build_equipment_response(kit):
    return {
        'id': kit['id'],
        'name': kit['name'],
        'brand': kit.get('brand', ''),
        'price': kit.get('price', 0),
        'quantity': kit.get('quantity', 1),
        'purchase_link': kit.get('purchase_link', ''),
    }
