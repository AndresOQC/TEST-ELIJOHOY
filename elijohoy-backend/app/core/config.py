import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base de la aplicación."""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Base de datos
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://elijohoy_user:elijohoy_password@db:5432/elijohoy_db'
    LOCAL_DATABASE_URL = 'postgresql://elijohoy_user:elijohoy_password@db:5432/elijohoy_db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL if os.environ.get('FLASK_ENV') == 'production' else LOCAL_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # 24 horas para desarrollo
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 2592000)))
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # CORS - Lee desde .env o usa valores por defecto según entorno
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:9000,http://127.0.0.1:9000').split(',')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME'))
    
    # Password Recovery - URL del frontend para reseteo de contraseña
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:9000')
    PASSWORD_RESET_URL = os.environ.get('PASSWORD_RESET_URL', FRONTEND_URL)
    PASSWORD_RESET_TOKEN_EXPIRES = int(os.environ.get('PASSWORD_RESET_TOKEN_EXPIRES', 3600))

class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    TESTING = False
    
    # En producción, usar las variables de entorno con prefijo PRODUCTION si existen
    DATABASE_URL = os.environ.get('PRODUCTION_DATABASE_URL', os.environ.get('DATABASE_URL'))
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    
    # URLs de producción
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://elijohoy.com')
    PASSWORD_RESET_URL = os.environ.get('PASSWORD_RESET_URL', FRONTEND_URL)
    
    # CORS para producción
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'https://elijohoy.com,https://www.elijohoy.com').split(',')

class TestingConfig(Config):
    """Configuración para testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)

# Diccionario de configuraciones
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}