import bcrypt
from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.usuario import Usuario
from app.models.token import Token

def hash_password(password):
    """Generar hash de password usando bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Verificar password contra hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def require_roles(*roles):
    """Decorador para requerir roles específicos."""
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = Usuario.query.get(current_user_id)
            
            if not user or not user.activo:
                return jsonify({'error': 'Usuario no encontrado o inactivo'}), 401
            
            user_roles = user.get_roles()
            if not any(role in user_roles for role in roles):
                return jsonify({'error': 'Permisos insuficientes'}), 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    """Obtener el usuario actual desde el JWT."""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id:
            return Usuario.query.get(current_user_id)
    except:
        pass
    return None

def is_token_revoked(jwt_payload):
    """Verificar si un token está revocado."""
    jti = jwt_payload['jti']
    return Token.is_token_revoked(jti)

def revoke_token(jti):
    """Revocar un token."""
    return Token.revoke_token(jti)