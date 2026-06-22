import json
from dtos.errors import abort


def validate_list_equipment(request):
    try:
        offset = int(request.args.get('_offset', 0))
        limit = int(request.args.get('_limit', 10))
    except ValueError:
        abort(400, '_offset y _limit deben ser enteros')
    if offset < 0 or limit < 1:
        abort(400, '_offset >= 0 y _limit >= 1')
    params = {'offset': offset, 'limit': limit}
    category = request.args.get('category')
    if category:
        if category == 'null':
            params['category'] = None
        else:
            params['category'] = category
    return params


def validate_create_equipment(request):
    data = request.get_json()
    if not data:
        abort(400, 'Body requerido')
    name = data.get('name')
    brand = data.get('brand')
    price = data.get('price')
    quantity = data.get('quantity', 1)
    purchase_link = data.get('purchase_link')
    category = data.get('category')
    description = data.get('description')
    image_url = data.get('image_url')
    details = data.get('details')
    if not name or price is None:
        abort(400, 'Campos requeridos: name, price')
    if details and isinstance(details, str):
        try:
            json.loads(details)
        except (json.JSONDecodeError, TypeError):
            pass
        details_str = details
    elif details:
        details_str = json.dumps(details)
    else:
        details_str = None
    result = {
        'name': name.strip(),
        'brand': brand.strip() if brand else None,
        'price': float(price),
        'quantity': int(quantity),
        'purchase_link': purchase_link.strip() if purchase_link else None,
        'category': category.strip() if category else None,
        'description': description.strip() if description else None,
        'image_url': image_url.strip() if image_url else None,
        'details': details_str,
    }
    return result


validate_replace_equipment = validate_create_equipment


def build_equipment_response(kit):
    details = kit.get('details')
    if details and isinstance(details, str):
        try:
            details = json.loads(details)
        except (json.JSONDecodeError, TypeError):
            details = None
    return {
        'id': kit['id'],
        'name': kit['name'],
        'category': kit.get('category', ''),
        'brand': kit.get('brand', ''),
        'description': kit.get('description', ''),
        'image_url': kit.get('image_url', ''),
        'price': kit.get('price', 0),
        'quantity': kit.get('quantity', 1),
        'purchase_link': kit.get('purchase_link', ''),
        'details': details,
        'sort_order': kit.get('sort_order', 0),
    }
