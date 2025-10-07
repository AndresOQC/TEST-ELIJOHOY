from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
import logging
from logging.handlers import RotatingFileHandler
import os

# Inicialización de extensiones
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
mail = Mail()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv("RATELIMIT_STORAGE_URL", "memory://")  # Use Redis from .env
)

# Set para almacenar tokens blacklistados
blacklisted_tokens = set()

def setup_logging(app):
    """Configurar el sistema de logging."""
    if not app.debug and not app.testing:
        # Crear directorio de logs si no existe
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configurar handler de archivo rotativo
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'], 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.info('ElijHoy Backend startup')

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Verificar si un token está en la blacklist."""
    from app.models.token import Token
    jti = jwt_payload['jti']
    return Token.is_token_revoked(jti)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Manejar tokens expirados."""
    return {
        'success': False,
        'message': 'Token expirado'
    }, 422

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Manejar tokens inválidos."""
    return {
        'success': False,
        'message': 'Token inválido'
    }, 422

@jwt.unauthorized_loader
def missing_token_callback(error):
    """Manejar tokens faltantes."""
    return {
        'success': False,
        'message': 'Token de autorización requerido'
    }, 401

def add_token_to_blacklist(jti):
    """Agregar un token a la blacklist."""
    blacklisted_tokens.add(jti)

def init_cors(app):
    from flask_cors import CORS
    import os

    cors = CORS()

    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    CORS(app, resources={r"/*": {"origins": allowed_origins}})