from flask import Flask, jsonify
from .config import config_by_name
from .extensions import db, jwt, cors, mail, limiter, setup_logging
import os

def create_app(config_name=None):
    """Factory para crear la aplicación Flask."""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object(config_by_name[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=[app.config['FRONTEND_URL']])
    mail.init_app(app)
    limiter.init_app(app)
    
    # Configurar logging
    setup_logging(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Registrar comandos CLI
    register_commands(app)
    
    # Manejadores de errores
    register_error_handlers(app)
    
    # Rutas básicas
    @app.route('/')
    def index():
        return jsonify({
            'message': 'ElijHoy Backend API',
            'version': '1.0.0',
            'status': 'running'
        })
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'database': 'connected' if db.engine else 'disconnected'
        })
    
    return app

def register_blueprints(app):
    """Registrar todos los blueprints."""
    from app.api.auth import auth_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

def register_commands(app):
    """Registrar comandos CLI."""
    from app.models.rol import Rol
    from app.models.usuario import Usuario
    from app.utils.auth_utils import hash_password
    import click
    
    @app.cli.command()
    def create_roles():
        """Crear roles por defecto."""
        with app.app_context():
            # Crear roles si no existen
            admin_role = Rol.query.filter_by(nombre='admin').first()
            if not admin_role:
                admin_role = Rol(nombre='admin', descripcion='Administrador del sistema')
                db.session.add(admin_role)
            
            student_role = Rol.query.filter_by(nombre='estudiante').first()
            if not student_role:
                student_role = Rol(nombre='estudiante', descripcion='Estudiante del sistema')
                db.session.add(student_role)
            
            db.session.commit()
            click.echo('Roles creados exitosamente.')
    
    @app.cli.command()
    @click.option('--email', prompt='Email del administrador')
    @click.option('--password', prompt='Password', hide_input=True)
    @click.option('--nombre', prompt='Nombre')
    @click.option('--apellidos', prompt='Apellidos')
    def create_admin(email, password, nombre, apellidos):
        """Crear usuario administrador."""
        with app.app_context():
            # Verificar si el usuario ya existe
            existing_user = Usuario.query.filter_by(email=email).first()
            if existing_user:
                click.echo('El usuario ya existe.')
                return
            
            # Crear usuario
            hashed_password = hash_password(password)
            admin_user = Usuario(
                email=email,
                password=hashed_password,
                nombre=nombre,
                apellidos=apellidos,
                activo=True
            )
            db.session.add(admin_user)
            db.session.flush()
            
            # Asignar rol de administrador
            admin_role = Rol.query.filter_by(nombre='admin').first()
            if admin_role:
                from app.models.usuario_rol import UsuarioRol
                user_role = UsuarioRol(usuario_id=admin_user.id, rol_id=admin_role.id)
                db.session.add(user_role)
            
            db.session.commit()
            click.echo('Usuario administrador creado exitosamente.')
    
    @app.cli.command()
    def cleanup_expired_tokens():
        """Limpiar tokens expirados."""
        with app.app_context():
            from app.models.token import Token
            from datetime import datetime
            
            # Eliminar tokens expirados
            expired_tokens = Token.query.filter(
                Token.fecha_expiracion < datetime.utcnow()
            ).all()
            
            count = len(expired_tokens)
            for token in expired_tokens:
                db.session.delete(token)
            
            db.session.commit()
            click.echo(f'Se eliminaron {count} tokens expirados.')

def register_error_handlers(app):
    """Registrar manejadores de errores."""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Recurso no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({'error': 'Demasiadas solicitudes. Inténtalo más tarde.'}), 429