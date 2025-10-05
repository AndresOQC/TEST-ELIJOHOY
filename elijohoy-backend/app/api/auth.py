from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, 
    create_refresh_token, get_jwt
)
from app.core.extensions import db, limiter
from app.models.usuario import Usuario
from app.models.alumno import Alumno
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol
from app.models.token import Token
from app.utils.auth_utils import hash_password, verify_password, get_current_user, revoke_token
from app.utils.validators import validate_user_data, sanitize_string
from app.utils.email_utils import send_password_reset_email
from datetime import datetime, timedelta
import uuid

# Crear blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """Endpoint para login de usuario."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No se enviaron datos'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email y password son requeridos'}), 400
        
        # Buscar usuario
        user = Usuario.query.filter_by(email=email).first()
        
        if not user or not user.activo:
            return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401
        
        # Verificar password
        if not verify_password(password, user.password_hash):
            return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401
        
        # Actualizar último acceso
        user.ultimo_login = datetime.utcnow()
        db.session.commit()
        
        # Crear tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Guardar tokens en BD (opcional, para tracking)
        # ... código para guardar tokens en BD si es necesario
        
        return jsonify({
            'success': True,
            'message': 'Login exitoso',
            'data': {
                'user': user.to_dict(include_roles=True),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error en login: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("3 per minute")
def register():
    """Endpoint para registro de nuevo usuario."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No se enviaron datos'}), 400
        
        # Validar datos
        errors = validate_user_data(data, is_registration=True)
        if errors:
            return jsonify({'success': False, 'message': '; '.join(errors)}), 400
        
        # Verificar si el usuario ya existe
        existing_user = Usuario.query.filter_by(email=data['email'].lower()).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'El email ya está registrado'}), 409
        
        # Crear usuario
        hashed_password = hash_password(data['password'])
        
        new_user = Usuario(
            email=data['email'].lower(),
            password_hash=hashed_password,
            activo=True,
            email_verificado=True
        )
        
        db.session.add(new_user)
        db.session.flush()  # Para obtener el ID
        
        # Asignar rol de estudiante por defecto
        student_role = Rol.query.filter_by(nombre='estudiante').first()
        if student_role:
            user_role = UsuarioRol(usuario_id=new_user.id, rol_id=student_role.id)
            db.session.add(user_role)
        
        # Crear perfil de alumno (obligatorio para registro)
        alumno = Alumno(
            usuario_id=new_user.id,
            nombre=sanitize_string(data['nombre'], 100),
            apellidos=sanitize_string(data['apellidos'], 100),
            edad=data['edad'],
            genero=data.get('genero', '').lower() if data.get('genero') else None,
            email=data['email'].lower(),
            ciudad=sanitize_string(data.get('ciudad'), 100),
            pais=sanitize_string(data.get('pais'), 100),
            institucion_educativa=sanitize_string(data.get('institucion_educativa'), 200),
            grado=sanitize_string(data.get('grado'), 50),
            seccion=sanitize_string(data.get('seccion'), 50),
            turno=sanitize_string(data.get('turno'), 50) if data.get('turno') else None
        )
        db.session.add(alumno)
        
        db.session.commit()
        
        # Crear tokens
        access_token = create_access_token(identity=new_user.id)
        refresh_token = create_refresh_token(identity=new_user.id)
        
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'data': {
                'user': new_user.to_dict(include_roles=True),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error en registro: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """Obtener información del usuario actual."""
    try:
        current_user_id = get_jwt_identity()
        current_app.logger.info(f'Obteniendo usuario con ID: {current_user_id}')
        
        if not current_user_id:
            return jsonify({'success': False, 'message': 'Token JWT inválido'}), 422
        
        user = Usuario.query.get(current_user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
            
        if not user.activo:
            return jsonify({'success': False, 'message': 'Usuario inactivo'}), 403
        
        try:
            user_data = user.to_dict(include_roles=True)
            current_app.logger.info(f'Usuario data generado correctamente para: {user.email}')
        except Exception as dict_error:
            current_app.logger.error(f'Error generando to_dict: {str(dict_error)}')
            # Datos básicos de fallback
            user_data = {
                'id': user.id,
                'email': user.email,
                'activo': user.activo
            }
        
        return jsonify({
            'success': True,
            'data': {
                'user': user_data
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error obteniendo usuario actual: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renovar access token usando refresh token."""
    try:
        current_user_id = get_jwt_identity()
        user = Usuario.query.get(current_user_id)
        
        if not user or not user.activo:
            return jsonify({'success': False, 'message': 'Usuario no encontrado o inactivo'}), 401
        
        # Crear nuevo access token
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'success': True,
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error renovando token: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Cerrar sesión del usuario."""
    try:
        jti = get_jwt()['jti']
        
        # Revocar el token
        revoke_token(jti)
        
        return jsonify({
            'success': True,
            'message': 'Sesión cerrada exitosamente'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error en logout: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Actualizar perfil del usuario."""
    try:
        user = get_current_user()
        if not user or not user.activo:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No se enviaron datos'}), 400
        
        # Actualizar datos de usuario
        if 'nombre' in data:
            user.nombre = sanitize_string(data['nombre'], 100)
        if 'apellidos' in data:
            user.apellidos = sanitize_string(data['apellidos'], 100)
        
        # Actualizar o crear perfil de alumno
        alumno = user.alumno
        if not alumno:
            alumno = Alumno(usuario_id=user.id)
            db.session.add(alumno)
        
        # Actualizar campos de alumno
        if 'edad' in data:
            alumno.edad = data.get('edad')
        if 'genero' in data:
            alumno.genero = data.get('genero', '').lower() if data.get('genero') else None
        if 'ciudad' in data:
            alumno.ciudad = sanitize_string(data.get('ciudad'), 100)
        if 'pais' in data:
            alumno.pais = sanitize_string(data.get('pais'), 100)
        if 'institucion_educativa' in data:
            alumno.institucion_educativa = sanitize_string(data.get('institucion_educativa'), 200)
        if 'grado' in data:
            alumno.grado = sanitize_string(data.get('grado'), 50)
        if 'seccion' in data:
            alumno.seccion = sanitize_string(data.get('seccion'), 10)
        if 'turno' in data:
            alumno.turno = sanitize_string(data.get('turno', '').lower() if data.get('turno') else None, 20)
        
        user.fecha_actualizacion = datetime.utcnow()
        alumno.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        user_data = user.to_dict(include_roles=True)
        if user.alumno:
            user_data['alumno'] = user.alumno.to_dict()
        
        return jsonify({
            'success': True,
            'message': 'Perfil actualizado exitosamente',
            'data': {'user': user_data}
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error actualizando perfil: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/recover-password', methods=['POST'])
@limiter.limit("3 per minute")
def recover_password():
    """Recuperar contraseña."""
    try:
        data = request.get_json()
        if not data or not data.get('email'):
            return jsonify({'success': False, 'message': 'Email es requerido'}), 400
        
        email = data['email'].strip().lower()
        user = Usuario.query.filter_by(email=email).first()
        
        if not user or not user.activo:
            # Por seguridad, siempre retornamos el mismo mensaje
            return jsonify({
                'success': True,
                'message': 'Si el email existe, recibirás instrucciones de recuperación'
            }), 200
        
        # Crear token de recuperación
        try:
            reset_token = Token.create_password_reset_token(
                user.id, 
                current_app.config['PASSWORD_RESET_TOKEN_EXPIRES']
            )
            
            # Enviar email de recuperación
            email_sent = send_password_reset_email(
                user_email=user.email,
                user_name=user.alumno.nombre if user.alumno else user.email,
                reset_token=reset_token.jti
            )
            
            if email_sent:
                current_app.logger.info(f'Email de recuperación enviado a {user.email}')
            else:
                current_app.logger.error(f'Error enviando email de recuperación a {user.email}')
            
            # Siempre retornamos éxito por seguridad
            return jsonify({
                'success': True,
                'message': 'Si el email existe, recibirás instrucciones de recuperación'
            }), 200
            
        except Exception as email_error:
            current_app.logger.error(f'Error procesando recuperación: {str(email_error)}')
            return jsonify({
                'success': True,
                'message': 'Si el email existe, recibirás instrucciones de recuperación'
            }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error en recuperación de contraseña: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/reset-password', methods=['POST'])
@limiter.limit("3 per minute")
def reset_password():
    """Restablecer contraseña con token."""
    try:
        data = request.get_json()
        if not data or not data.get('token') or not data.get('new_password'):
            return jsonify({'success': False, 'message': 'Token y nueva contraseña son requeridos'}), 400
        
        token_string = data['token']
        new_password = data['new_password']
        
        # Validar la nueva contraseña
        password_errors = []
        if len(new_password) < 8:
            password_errors.append('La contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in new_password):
            password_errors.append('La contraseña debe contener al menos una mayúscula')
        if not any(c.islower() for c in new_password):
            password_errors.append('La contraseña debe contener al menos una minúscula')
        if not any(c.isdigit() for c in new_password):
            password_errors.append('La contraseña debe contener al menos un número')
        if not any(c in '!@#$%^&*(),.?":{}|<>' for c in new_password):
            password_errors.append('La contraseña debe contener al menos un símbolo')
        
        if password_errors:
            return jsonify({
                'success': False, 
                'message': 'Contraseña no válida',
                'errors': password_errors
            }), 400
        
        # Verificar el token
        reset_token = Token.verify_password_reset_token(token_string)
        
        if not reset_token:
            return jsonify({
                'success': False,
                'message': 'Token inválido o expirado'
            }), 400
        
        # Obtener el usuario
        user = Usuario.query.get(reset_token.usuario_id)
        if not user or not user.activo:
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 404
        
        # Cambiar la contraseña
        user.password_hash = hash_password(new_password)
        user.actualizado_en = datetime.utcnow()
        
        # Marcar el token como usado
        reset_token.use_token()
        
        # Revocar todos los tokens JWT activos del usuario
        existing_tokens = Token.query.filter_by(usuario_id=user.id, revocado=False).all()
        for token in existing_tokens:
            token.revocado = True
        
        db.session.commit()
        
        current_app.logger.info(f'Contraseña restablecida para usuario {user.email}')
        
        return jsonify({
            'success': True,
            'message': 'Contraseña restablecida exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error restableciendo contraseña: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500