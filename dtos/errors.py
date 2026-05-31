from functools import wraps
from flask import jsonify, request as flask_request, g
from flask_jwt_extended import get_jwt
from werkzeug.exceptions import HTTPException
from flask import abort as flask_abort


def abort(code, message):
    flask_abort(code, description=message)


def validate_dto(validator):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                g.dto = validator(flask_request)
                return func(*args, **kwargs)
            except HTTPException as e:
                return jsonify({'errors': [{
                    'code': e.code,
                    'message': e.description,
                    'level': 'error',
                }]}), e.code
        return wrapper
    return decorator


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_jwt().get('is_admin'):
            abort(403, 'Solo administradores pueden realizar esta acción')
        return func(*args, **kwargs)
    return wrapper
