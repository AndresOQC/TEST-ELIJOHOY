from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, 
    create_refresh_token, get_jwt, decode_token
)
from app.core.extensions import db, limiter
from app.models.usuario import Usuario
from app.models.alumno import Alumno
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol
from app.models.token import Token
from app.models.sesion_test import SesionTest
from app.utils.auth_utils import hash_password, verify_password, get_current_user, revoke_token
from app.utils.validators import validate_user_data, sanitize_string
from app.utils.email_utils import send_password_reset_email
from datetime import datetime, timedelta
import uuid
import traceback

# Crear blueprint
auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/usuarios/buscar-por-email', methods=['POST'])
def buscar_usuario_por_email():
    """Buscar usuario por email y devolver su id."""
    try:
        data = request.get_json(force=True, silent=True)
        email = data.get('email') if data else None
        if not email:
            return jsonify({'success': False, 'message': 'Email requerido'}), 400
        usuario = Usuario.query.filter_by(email=email.lower()).first()
        if not usuario:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
        return jsonify({'success': True, 'id_usuario': usuario.id}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Protección contra ataques de fuerza bruta
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

        # Crear tokens JWT
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        # Guardar tokens en BD
        try:
            access_jti = decode_token(access_token)['jti']
            refresh_jti = decode_token(refresh_token)['jti']
        except Exception as e:
            current_app.logger.error(f'Error descodificando tokens: {str(e)}')
            return jsonify({'success': False, 'message': 'Error al generar tokens'}), 500

        # Usar configuración de duración de tokens
        access_expires = datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        refresh_expires = datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']

        token_access = Token(
            usuario_id=user.id,
            jti=access_jti,
            tipo='access',
            fecha_expiracion=access_expires
        )
        token_refresh = Token(
            usuario_id=user.id,
            jti=refresh_jti,
            tipo='refresh',
            fecha_expiracion=refresh_expires
        )

        db.session.add(token_access)
        db.session.add(token_refresh)

        db.session.commit()

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
        db.session.rollback()
        current_app.logger.error(f'Error en login: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("3 per minute")  # Protección contra ataques de fuerza bruta
def register():
    """Endpoint para registro de nuevo usuario."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': 'No se enviaron datos'}), 400

        # Validar datos
        errors = validate_user_data(data, is_registration=True)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400

        # Validar que `nombre`, `apellidos` y `edad` estén presentes
        nombre = data.get('nombre')
        apellidos = data.get('apellidos')
        edad = data.get('edad')

        if not nombre or not apellidos:
            return jsonify({'success': False, 'message': 'Los campos nombre y apellidos son requeridos'}), 400

        if not edad:
            return jsonify({'success': False, 'message': 'El campo edad es requerido'}), 400

        # Crear usuario
        nuevo_usuario = Usuario(
            email=data['email'].lower(),
            password_hash=hash_password(data['password']),
            activo=True
        )
        db.session.add(nuevo_usuario)
        db.session.flush()  # Obtener el ID sin hacer commit completo

        # Crear alumno asociado
        nuevo_alumno = Alumno(
            usuario_id=nuevo_usuario.id,
            nombre=nombre,
            apellidos=apellidos,
            edad=edad,
            email=data['email'].lower(),
            genero=data.get('genero'),
            ciudad=data.get('ciudad'),
            pais=data.get('pais'),
            institucion_educativa=data.get('institucion_educativa'),
            grado=data.get('grado'),
            seccion=data.get('seccion'),
            turno=data.get('turno')
        )
        db.session.add(nuevo_alumno)

        # Asignar rol de alumno por defecto
        rol_alumno = Rol.query.filter_by(nombre='alumno').first()
        if rol_alumno:
            usuario_rol = UsuarioRol(usuario_id=nuevo_usuario.id, rol_id=rol_alumno.id)
            db.session.add(usuario_rol)

        db.session.commit()

        # Verificar que el usuario tenga ID válido
        if not nuevo_usuario.id:
            return jsonify({'success': False, 'message': 'Error al crear usuario'}), 500

        # Crear tokens JWT
        access_token = create_access_token(identity=str(nuevo_usuario.id))
        refresh_token = create_refresh_token(identity=str(nuevo_usuario.id))

        # Guardar tokens en BD
        try:
            access_jti = decode_token(access_token)['jti']
            refresh_jti = decode_token(refresh_token)['jti']
        except Exception as e:
            current_app.logger.error(f'Error descodificando tokens: {str(e)}')
            return jsonify({'success': False, 'message': 'Error al generar tokens'}), 500

        # Usar configuración de duración de tokens
        access_expires = datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        refresh_expires = datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']

        token_access = Token(
            usuario_id=nuevo_usuario.id,
            jti=access_jti,
            tipo='access',
            fecha_expiracion=access_expires
        )
        token_refresh = Token(
            usuario_id=nuevo_usuario.id,
            jti=refresh_jti,
            tipo='refresh',
            fecha_expiracion=refresh_expires
        )

        db.session.add(token_access)
        db.session.add(token_refresh)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Registro exitoso',
            'data': {
                'user': nuevo_usuario.to_dict(include_roles=True),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 201

    except Exception as e:
        current_app.logger.error(f'Error en registro: {str(e)}')
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """Obtener información del usuario actual."""
    try:
        current_user_id = get_jwt_identity()
        
        try:
            current_user_id_int = int(current_user_id) if current_user_id else None
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'ID de usuario inválido'}), 401
        
        if not current_user_id_int:
            return jsonify({'success': False, 'message': 'Token JWT inválido'}), 422
        
        user = Usuario.query.get(current_user_id_int)
        
        if not user:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
            
        if not user.activo:
            return jsonify({'success': False, 'message': 'Usuario inactivo'}), 403
        
        try:
            user_data = user.to_dict(include_roles=True)
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
        try:
            current_user_id_int = int(current_user_id) if current_user_id else None
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'ID de usuario inválido'}), 401
        
        user = Usuario.query.get(current_user_id_int)
        
        if not user or not user.activo:
            return jsonify({'success': False, 'message': 'Usuario no encontrado o inactivo'}), 401
        
        # Crear nuevo access token
        new_access_token = create_access_token(identity=str(current_user_id_int))

        # Guardar token en BD con error handling
        try:
            access_jti = decode_token(new_access_token)['jti']
        except Exception as e:
            current_app.logger.error(f'Error descodificando token: {str(e)}')
            return jsonify({'success': False, 'message': 'Error al generar token'}), 500
        
        # Usar configuración de duración
        access_expires = datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']

        token_access = Token(
            usuario_id=current_user_id_int,
            jti=access_jti,
            tipo='access',
            fecha_expiracion=access_expires
        )
        db.session.add(token_access)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Token renovado exitosamente',
            'data': {
                'access_token': new_access_token
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error renovando token: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Cerrar sesión del usuario."""
    try:
        jti = get_jwt()['jti']

        # Revocar el token en la base de datos
        Token.revoke_token(jti)

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
        
        # Actualizar o crear perfil de alumno
        alumno = user.alumno
        if not alumno:
            alumno = Alumno(usuario_id=user.id)
            db.session.add(alumno)
        
        # Actualizar campos de alumno
        if 'nombre' in data:
            alumno.nombre = sanitize_string(data['nombre'], 100)
        if 'apellidos' in data:
            alumno.apellidos = sanitize_string(data['apellidos'], 100)
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
        
        # No es necesario actualizar manualmente actualizado_en - SQLAlchemy lo hace automáticamente
        
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
@limiter.limit("3 per minute")  # Protección contra ataques de fuerza bruta
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
            
            # Determinar el nombre del usuario para el email
            if user.alumno and user.alumno.nombre:
                user_name = f"{user.alumno.nombre} {user.alumno.apellidos}" if user.alumno.apellidos else user.alumno.nombre
            else:
                user_name = user.email.split('@')[0]  # Usar la parte del email antes del @
            
            # Enviar email de recuperación
            email_sent = send_password_reset_email(
                user_email=user.email,
                user_name=user_name,
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
@limiter.limit("3 per minute")  # Protección contra ataques de fuerza bruta
def reset_password():
    """Restablecer contraseña con token."""
    try:
        current_app.logger.info('=== Inicio reset-password ===')
        data = request.get_json()
        current_app.logger.info(f'Data recibida: {data}')
        
        if not data or not data.get('token') or not data.get('new_password'):
            return jsonify({'success': False, 'message': 'Token y nueva contraseña son requeridos'}), 400
        
        token_string = data['token']
        new_password = data['new_password']
        current_app.logger.info(f'Token recibido: {token_string[:20]}...')
        
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
            current_app.logger.warning(f'Errores de validación de contraseña: {password_errors}')
            return jsonify({
                'success': False, 
                'message': 'Contraseña no válida',
                'errors': password_errors
            }), 400
        
        # Verificar el token
        current_app.logger.info('Verificando token...')
        reset_token = Token.verify_password_reset_token(token_string)
        
        if not reset_token:
            current_app.logger.warning('Token inválido o expirado')
            return jsonify({
                'success': False,
                'message': 'Token inválido o expirado'
            }), 400
        
        current_app.logger.info(f'Token válido para usuario_id: {reset_token.usuario_id}')
        
        # Obtener el usuario
        user = Usuario.query.get(reset_token.usuario_id)
        if not user or not user.activo:
            current_app.logger.warning(f'Usuario no encontrado o inactivo: {reset_token.usuario_id}')
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 404
        
        current_app.logger.info(f'Usuario encontrado: {user.email}')
        
        # Cambiar la contraseña
        user.password_hash = hash_password(new_password)
        user.actualizado_en = datetime.utcnow()
        current_app.logger.info('Contraseña hasheada y usuario actualizado')
        
        # Marcar el token como usado
        reset_token.use_token()
        current_app.logger.info('Token marcado como usado')
        
        # Revocar todos los tokens JWT activos del usuario
        existing_tokens = Token.query.filter_by(usuario_id=user.id, revocado=False).all()
        for token in existing_tokens:
            token.revocado = True
        current_app.logger.info(f'Revocados {len(existing_tokens)} tokens JWT')
        
        db.session.commit()
        current_app.logger.info('Cambios guardados en BD')
        
        current_app.logger.info(f'Contraseña restablecida para usuario {user.email}')
        
        return jsonify({
            'success': True,
            'message': 'Contraseña restablecida exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error restableciendo contraseña: {str(e)}')
        current_app.logger.error(f'Tipo de error: {type(e).__name__}')
        import traceback
        current_app.logger.error(f'Traceback: {traceback.format_exc()}')
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500