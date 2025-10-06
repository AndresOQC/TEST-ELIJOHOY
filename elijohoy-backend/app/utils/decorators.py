from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.usuario import Usuario

def role_required(*roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles especificados.
    Uso: @role_required('administrador', 'alumno')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()

            usuario = Usuario.query.get(user_id)
            if not usuario:
                return jsonify({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }), 404

            user_roles = usuario.get_roles()

            # Verificar si el usuario tiene alguno de los roles requeridos
            if not any(role in user_roles for role in roles):
                return jsonify({
                    'success': False,
                    'message': 'No tienes permisos para acceder a este recurso'
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn):
    """
    Decorador para verificar que el usuario sea administrador.
    Uso: @admin_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()

        usuario = Usuario.query.get(user_id)
        if not usuario:
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 404

        if not usuario.has_role('administrador'):
            return jsonify({
                'success': False,
                'message': 'Acceso denegado. Se requieren permisos de administrador'
            }), 403

        return fn(*args, **kwargs)
    return wrapper


def alumno_or_admin_required(fn):
    """
    Decorador para verificar que el usuario sea alumno o administrador.
    Uso: @alumno_or_admin_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()

        usuario = Usuario.query.get(user_id)
        if not usuario:
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 404

        if not (usuario.has_role('administrador') or usuario.has_role('alumno')):
            return jsonify({
                'success': False,
                'message': 'Acceso denegado'
            }), 403

        return fn(*args, **kwargs)
    return wrapper


def is_owner_or_admin(user_id, resource_user_id):
    """
    Verificar si el usuario es propietario del recurso o es administrador.

    Args:
        user_id: ID del usuario actual
        resource_user_id: ID del usuario propietario del recurso

    Returns:
        bool: True si es propietario o admin, False en caso contrario
    """
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return False

    # Es administrador o es el propietario
    return usuario.has_role('administrador') or user_id == resource_user_id
