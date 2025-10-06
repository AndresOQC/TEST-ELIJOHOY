from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request, decode_token
from app.core.extensions import db, limiter
from app.utils.decorators import admin_required, role_required, is_owner_or_admin
from app.models.usuario import Usuario
from app.models.pregunta import Pregunta
from app.models.sesion_test import SesionTest
from app.models.respuesta import Respuesta
from app.models.tipo_personalidad import TipoPersonalidad
from sqlalchemy import text
import secrets

bp = Blueprint('test_personalidad', __name__, url_prefix='/api/test')


@bp.route('/buscar-sesion', methods=['POST'])
def buscar_sesion_por_id():
    """Buscar sesión por id_sesion y devolver id_sesion y id_usuario."""
    data = request.get_json()
    id_sesion = data.get('id_sesion')
    if not id_sesion:
        return jsonify({'success': False, 'message': 'id_sesion requerido'}), 400
    sesion = SesionTest.query.get(id_sesion)
    if not sesion:
        return jsonify({'success': False, 'message': 'Sesión no encontrada'}), 404
    return jsonify({
        'success': True,
        'id_sesion': sesion.id_sesion,
        'id_usuario': sesion.id_usuario
    }), 200


@bp.route('/preguntas', methods=['GET'])
@limiter.limit("10 per minute")
def obtener_preguntas():
    """Obtener todas las preguntas activas del test ordenadas."""
    try:
        preguntas = Pregunta.query.filter_by(activa=True).order_by(Pregunta.orden).all()
        return jsonify({
            'success': True,
            'preguntas': [p.to_dict() for p in preguntas]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener preguntas: {str(e)}'
        }), 500


@bp.route('/admin/preguntas', methods=['GET'])
@jwt_required()
@admin_required
def obtener_todas_preguntas():
    """Obtener todas las preguntas (activas e inactivas) para administración."""
    try:
        preguntas = Pregunta.query.order_by(Pregunta.orden).all()
        return jsonify({
            'success': True,
            'preguntas': [p.to_dict() for p in preguntas]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener preguntas: {str(e)}'
        }), 500


@bp.route('/admin/preguntas', methods=['POST'])
@jwt_required()
@admin_required
def crear_pregunta():
    """Crear una nueva pregunta."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': 'No se enviaron datos'}), 400

        # Validar campos requeridos
        texto_izquierda = data.get('texto_izquierda')
        texto_derecha = data.get('texto_derecha')
        dimension = data.get('dimension')
        peso = data.get('peso')
        orden = data.get('orden')

        if not texto_izquierda or not texto_derecha:
            return jsonify({'success': False, 'message': 'Los textos izquierda y derecha son requeridos'}), 400

        if not dimension or dimension not in ['IE', 'SN', 'FT', 'JP']:
            return jsonify({'success': False, 'message': 'La dimensión debe ser IE, SN, FT o JP'}), 400

        if peso not in [-1, 1]:
            return jsonify({'success': False, 'message': 'El peso debe ser -1 o 1'}), 400

        if orden is None:
            return jsonify({'success': False, 'message': 'El orden de la pregunta es requerido'}), 400

        # Verificar que el orden no esté duplicado
        pregunta_existente = Pregunta.query.filter_by(orden=orden).first()
        if pregunta_existente:
            return jsonify({'success': False, 'message': f'Ya existe una pregunta con el orden {orden}'}), 400

        # Crear nueva pregunta
        nueva_pregunta = Pregunta(
            texto_izquierda=texto_izquierda.strip(),
            texto_derecha=texto_derecha.strip(),
            dimension=dimension,
            peso=peso,
            orden=orden,
            activa=data.get('activa', True)
        )

        db.session.add(nueva_pregunta)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Pregunta creada exitosamente',
            'pregunta': nueva_pregunta.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al crear pregunta: {str(e)}'
        }), 500


@bp.route('/admin/preguntas/<int:id_pregunta>', methods=['PUT'])
@jwt_required()
@admin_required
def actualizar_pregunta(id_pregunta):
    """Actualizar una pregunta existente."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': 'No se enviaron datos'}), 400

        # Buscar la pregunta
        pregunta = Pregunta.query.get(id_pregunta)
        if not pregunta:
            return jsonify({'success': False, 'message': 'Pregunta no encontrada'}), 404

        # Validar y actualizar campos
        if 'texto_izquierda' in data:
            texto_izquierda = data['texto_izquierda']
            if not texto_izquierda or not texto_izquierda.strip():
                return jsonify({'success': False, 'message': 'El texto izquierda no puede estar vacío'}), 400
            pregunta.texto_izquierda = texto_izquierda.strip()

        if 'texto_derecha' in data:
            texto_derecha = data['texto_derecha']
            if not texto_derecha or not texto_derecha.strip():
                return jsonify({'success': False, 'message': 'El texto derecha no puede estar vacío'}), 400
            pregunta.texto_derecha = texto_derecha.strip()

        if 'dimension' in data:
            dimension = data['dimension']
            if not dimension or dimension not in ['IE', 'SN', 'FT', 'JP']:
                return jsonify({'success': False, 'message': 'La dimensión debe ser IE, SN, FT o JP'}), 400
            pregunta.dimension = dimension

        if 'peso' in data:
            peso = data['peso']
            if peso not in [-1, 1]:
                return jsonify({'success': False, 'message': 'El peso debe ser -1 o 1'}), 400
            pregunta.peso = peso

        if 'orden' in data:
            nuevo_orden = data['orden']
            if nuevo_orden is None:
                return jsonify({'success': False, 'message': 'El orden no puede ser nulo'}), 400

            # Verificar que el nuevo orden no esté duplicado (excepto para la misma pregunta)
            pregunta_existente = Pregunta.query.filter_by(orden=nuevo_orden).filter(Pregunta.id_pregunta != id_pregunta).first()
            if pregunta_existente:
                return jsonify({'success': False, 'message': f'Ya existe una pregunta con el orden {nuevo_orden}'}), 400

            pregunta.orden = nuevo_orden

        if 'activa' in data:
            pregunta.activa = bool(data['activa'])

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Pregunta actualizada exitosamente',
            'pregunta': pregunta.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al actualizar pregunta: {str(e)}'
        }), 500


@bp.route('/admin/preguntas/<int:id_pregunta>', methods=['DELETE'])
@jwt_required()
@admin_required
def eliminar_pregunta(id_pregunta):
    """Eliminar (desactivar) una pregunta."""
    try:
        pregunta = Pregunta.query.get(id_pregunta)
        if not pregunta:
            return jsonify({'success': False, 'message': 'Pregunta no encontrada'}), 404

        # En lugar de eliminar físicamente, la desactivamos
        pregunta.activa = False
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Pregunta desactivada exitosamente'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al eliminar pregunta: {str(e)}'
        }), 500


@bp.route('/iniciar', methods=['POST'])
@limiter.limit("10 per minute")
@jwt_required(optional=True)
def iniciar_test():
    """Iniciar una nueva sesión de test (anónima o autenticada)."""
    try:
        # Obtener datos de la solicitud
        data = request.get_json() or {}
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent')

        # Log de headers para debugging
        auth_header = request.headers.get('Authorization')
        current_app.logger.info(f'Headers de petición: Authorization={auth_header}')

        # Verificar si el usuario está autenticado
        id_usuario = None
        try:
            id_usuario_str = get_jwt_identity()
            id_usuario = int(id_usuario_str) if id_usuario_str else None
            current_app.logger.info(f'✅ Usuario autenticado en /iniciar: {id_usuario} (string: {id_usuario_str})')
        except Exception as e:
            current_app.logger.info(f'❌ Usuario no autenticado en /iniciar: {str(e)}')
            pass

        # Generar token anónimo si no está autenticado
        token_anonimo = None
        if not id_usuario:
            # Generar token aleatorio único
            while True:
                token_anonimo = secrets.token_hex(32)
                existe = SesionTest.query.filter_by(token_anonimo=token_anonimo).first()
                if not existe:
                    break

        # Crear nueva sesión
        nueva_sesion = SesionTest(
            id_usuario=id_usuario,
            token_anonimo=token_anonimo,
            ip_address=ip_address,
            user_agent=user_agent
        )

        db.session.add(nueva_sesion)
        db.session.commit()

        current_app.logger.info(f'Sesión creada: id={nueva_sesion.id_sesion}, usuario={id_usuario}')

        return jsonify({
            'success': True,
            'sesion': nueva_sesion.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al iniciar test: {str(e)}'
        }), 500


@bp.route('/responder', methods=['POST'])
@limiter.limit("100 per minute")
def guardar_respuesta():
    """Guardar una respuesta individual del test."""
    try:
        data = request.get_json()

        # Validar datos requeridos
        if not data or 'id_sesion' not in data or 'id_pregunta' not in data or 'valor_respuesta' not in data:
            return jsonify({
                'success': False,
                'message': 'Faltan datos requeridos: id_sesion, id_pregunta, valor_respuesta'
            }), 400

        id_sesion = data['id_sesion']
        id_pregunta = data['id_pregunta']
        valor_respuesta = data['valor_respuesta']
        tiempo_respuesta = data.get('tiempo_respuesta')

        # Validar que la sesión existe y no está completada
        sesion = SesionTest.query.get(id_sesion)
        if not sesion:
            return jsonify({
                'success': False,
                'message': 'Sesión no encontrada'
            }), 404

        if sesion.completado:
            return jsonify({
                'success': False,
                'message': 'La sesión ya está completada'
            }), 400

        # Validar que la pregunta existe
        pregunta = Pregunta.query.get(id_pregunta)
        if not pregunta or not pregunta.activa:
            return jsonify({
                'success': False,
                'message': 'Pregunta no válida'
            }), 400

        # Validar valor de respuesta (1-5)
        if not isinstance(valor_respuesta, int) or valor_respuesta < 1 or valor_respuesta > 5:
            return jsonify({
                'success': False,
                'message': 'El valor de respuesta debe estar entre 1 y 5'
            }), 400

        # Verificar si ya existe una respuesta para esta pregunta en esta sesión
        respuesta_existente = Respuesta.query.filter_by(
            id_sesion=id_sesion,
            id_pregunta=id_pregunta
        ).first()

        if respuesta_existente:
            # Actualizar respuesta existente
            respuesta_existente.valor_respuesta = valor_respuesta
            respuesta_existente.tiempo_respuesta = tiempo_respuesta
            respuesta = respuesta_existente
        else:
            # Crear nueva respuesta
            respuesta = Respuesta(
                id_sesion=id_sesion,
                id_pregunta=id_pregunta,
                valor_respuesta=valor_respuesta,
                tiempo_respuesta=tiempo_respuesta
            )
            db.session.add(respuesta)

        db.session.commit()

        # Contar respuestas para verificar si está completo
        total_respuestas = sesion.contar_respuestas()

        return jsonify({
            'success': True,
            'respuesta': respuesta.to_dict(),
            'progreso': {
                'respondidas': total_respuestas,
                'total': 32,
                'completado': total_respuestas == 32
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al guardar respuesta: {str(e)}'
        }), 500


@bp.route('/finalizar/<int:id_sesion>', methods=['POST'])
@limiter.limit("5 per minute")
def finalizar_test(id_sesion):
    """Finalizar test y calcular resultados."""
    try:
        sesion = SesionTest.query.get(id_sesion)
        if not sesion:
            return jsonify({
                'success': False,
                'message': 'Sesión no encontrada'
            }), 404

        if sesion.completado:
            return jsonify({
                'success': False,
                'message': 'La sesión ya está completada'
            }), 400

        if not sesion.esta_completa():
            respuestas_count = sesion.contar_respuestas()
            current_app.logger.warning(f'Sesión {id_sesion} incompleta: {respuestas_count}/32 respuestas.')
            return jsonify({
                'success': False,
                'message': f'Test incompleto. Respuestas: {respuestas_count}/32'
            }), 400

        result = db.session.execute(
            text("SELECT * FROM calcular_resultados_test(:id_sesion)"),
            {'id_sesion': id_sesion}
        ).fetchone()

        db.session.commit()  # Asegurar que los cambios se guarden
        db.session.refresh(sesion)

        return jsonify({
            'success': True,
            'resultados': sesion.to_dict(include_tipo=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al finalizar test {id_sesion}: {str(e)}')
        return jsonify({
            'success': False,
            'message': f'Error al finalizar test: {str(e)}'
        }), 500


@bp.route('/resultados/<int:id_sesion>', methods=['GET'])
def obtener_resultados(id_sesion):
    """Obtener resultados detallados de una sesión completada."""
    try:
        sesion = SesionTest.query.get(id_sesion)
        if not sesion:
            return jsonify({
                'success': False,
                'message': 'Sesión no encontrada'
            }), 404

        # Verificar permisos si hay usuario autenticado
        try:
            verify_jwt_in_request(optional=True)
            id_usuario_str = get_jwt_identity()
            id_usuario = int(id_usuario_str) if id_usuario_str else None

            if id_usuario:
                # Si está autenticado, verificar que sea el propietario o admin
                if not is_owner_or_admin(id_usuario, sesion.id_usuario):
                    return jsonify({
                        'success': False,
                        'message': 'No tienes permiso para ver estos resultados'
                    }), 403
        except Exception as e:
            current_app.logger.warning(f'Error en verificación JWT: {str(e)}')
            # Si la sesión no tiene usuario (es anónima), permitir acceso
            if sesion.id_usuario is not None:
                return jsonify({
                    'success': False,
                    'message': 'Acceso denegado'
                }), 403

        if not sesion.completado:
            return jsonify({
                'success': False,
                'message': 'Test no completado'
            }), 400

        # Obtener perfil completo usando la función PostgreSQL
        result = db.session.execute(
            text("SELECT obtener_perfil_usuario(:id_sesion)"),
            {'id_sesion': id_sesion}
        ).scalar()

        return jsonify({
            'success': True,
            'perfil': result
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener resultados: {str(e)}'
        }), 500


@bp.route('/mis-sesiones', methods=['GET'])
@jwt_required()
@role_required('alumno', 'administrador')
def obtener_mis_sesiones():
    """Obtener todas las sesiones del usuario autenticado (alumno solo ve las suyas)."""
    try:
        id_usuario_str = get_jwt_identity()
        id_usuario = int(id_usuario_str) if id_usuario_str else None
        usuario = Usuario.query.get(id_usuario)

        # Alumno solo puede ver sus propias sesiones
        if not usuario.has_role('administrador'):
            sesiones = SesionTest.query.filter_by(id_usuario=id_usuario)\
                .order_by(SesionTest.fecha_inicio.desc())\
                .all()
        else:
            # Administrador ve todas las sesiones
            sesiones = SesionTest.query\
                .order_by(SesionTest.fecha_inicio.desc())\
                .all()

        return jsonify({
            'success': True,
            'sesiones': [s.to_dict(include_tipo=True, include_usuario=usuario.has_role('administrador')) for s in sesiones]
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener sesiones: {str(e)}'
        }), 500


@bp.route('/asociar-sesion', methods=['POST'])
@jwt_required()
def asociar_sesion_anonima():
    """Asociar una sesión anónima al usuario actual tras registro."""
    try:
        data = request.get_json(force=True, silent=True)
        id_usuario_str = get_jwt_identity()
        id_usuario = int(id_usuario_str) if id_usuario_str else None

        if not data or 'id_sesion' not in data:
            current_app.logger.error('id_sesion faltante o JSON mal formado.')
            return jsonify({
                'success': False,
                'message': 'id_sesion requerido (JSON mal formado o campo faltante)'
            }), 400

        id_sesion = data['id_sesion']
        if not id_sesion or not isinstance(id_sesion, int):
            current_app.logger.error('id_sesion vacío o inválido.')
            return jsonify({
                'success': False,
                'message': 'id_sesion vacío o inválido'
            }), 400

        current_app.logger.info(f'id_sesion recibido: {id_sesion}')

        # Buscar sesión
        sesion = SesionTest.query.get(id_sesion)
        current_app.logger.info(f'Sesión encontrada: {sesion}')

        if not sesion:
            current_app.logger.error('Sesión no encontrada.')
            return jsonify({
                'success': False,
                'message': 'Sesión no encontrada'
            }), 404

        # Asociar al usuario
        sesion.id_usuario = id_usuario
        db.session.commit()

        current_app.logger.info(f'Sesión asociada al usuario: {id_usuario}')
        return jsonify({
            'success': True,
            'sesion': sesion.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al asociar sesión: {str(e)}')
        return jsonify({
            'success': False,
            'message': f'Error al asociar sesión: {str(e)}'
        }), 500


@bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@admin_required
def obtener_estadisticas():
    """Obtener estadísticas generales del sistema (solo admin)."""
    try:
        # Obtener estadísticas usando la función PostgreSQL
        result = db.session.execute(text("SELECT estadisticas_sistema()")).scalar()

        return jsonify({
            'success': True,
            'estadisticas': result
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estadísticas: {str(e)}'
        }), 500


@bp.route('/admin/sesiones', methods=['GET'])
@jwt_required()
@admin_required
def obtener_todas_sesiones():
    """Obtener todas las sesiones del sistema (solo admin)."""
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        completado = request.args.get('completado', None, type=lambda v: v.lower() == 'true')

        # Query base
        query = SesionTest.query

        # Filtrar por completado si se especifica
        if completado is not None:
            query = query.filter_by(completado=completado)

        # Ordenar por fecha más reciente
        query = query.order_by(SesionTest.fecha_inicio.desc())

        # Paginar
        sesiones_paginadas = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'success': True,
            'sesiones': [s.to_dict(include_tipo=True) for s in sesiones_paginadas.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': sesiones_paginadas.total,
                'pages': sesiones_paginadas.pages
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener sesiones: {str(e)}'
        }), 500


@bp.route('/admin/usuarios/<int:id_usuario>/sesiones', methods=['GET'])
@jwt_required()
@admin_required
def obtener_sesiones_usuario(id_usuario):
    """Obtener todas las sesiones de un usuario específico (solo admin)."""
    try:
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 404

        sesiones = SesionTest.query.filter_by(id_usuario=id_usuario)\
            .order_by(SesionTest.fecha_inicio.desc())\
            .all()

        return jsonify({
            'success': True,
            'usuario': usuario.to_dict(),
            'sesiones': [s.to_dict(include_tipo=True) for s in sesiones]
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener sesiones del usuario: {str(e)}'
        }), 500


@bp.route('/tipos', methods=['GET'])
def obtener_tipos_personalidad():
    """Obtener todos los tipos de personalidad."""
    try:
        tipos = TipoPersonalidad.query.all()
        return jsonify({
            'success': True,
            'tipos': [t.to_dict() for t in tipos]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener tipos: {str(e)}'
        }), 500


@bp.route('/tipos/<string:codigo>', methods=['GET'])
def obtener_tipo_por_codigo(codigo):
    """Obtener información detallada de un tipo específico."""
    try:
        tipo = TipoPersonalidad.query.get(codigo.upper())
        if not tipo:
            return jsonify({
                'success': False,
                'message': 'Tipo de personalidad no encontrado'
            }), 404

        return jsonify({
            'success': True,
            'tipo': tipo.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener tipo: {str(e)}'
        }), 500


# ============ ENDPOINTS DE ADMINISTRACIÓN DE PREGUNTAS ============


@bp.route('/admin/preguntas/<int:id_pregunta>/toggle', methods=['PATCH'])
@jwt_required()
@admin_required
def toggle_pregunta_activa(id_pregunta):
    """Activar/desactivar una pregunta (solo admin)."""
    try:
        pregunta = Pregunta.query.get(id_pregunta)
        if not pregunta:
            return jsonify({
                'success': False,
                'message': 'Pregunta no encontrada'
            }), 404

        data = request.get_json()
        pregunta.activa = data.get('activa', not pregunta.activa)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Pregunta {"activada" if pregunta.activa else "desactivada"} exitosamente',
            'pregunta': pregunta.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al actualizar estado: {str(e)}'
        }), 500

@bp.route('/admin/sesiones/reenviar-token', methods=['POST'])
@jwt_required()
@admin_required
def reenviar_token_sesion():
    """Reenviar el token de una sesión a un usuario (solo admin)."""
    try:
        data = request.get_json()
        id_sesion = data.get('id_sesion')
        email_usuario = data.get('email_usuario')

        if not id_sesion or not email_usuario:
            return jsonify({
                'success': False,
                'message': 'Faltan datos requeridos: id_sesion, email_usuario'
            }), 400

        # Buscar sesión
        sesion = SesionTest.query.get(id_sesion)
        if not sesion:
            return jsonify({
                'success': False,
                'message': 'Sesión no encontrada'
            }), 404

        # Enviar correo electrónico con el token
        # Aquí se debe implementar el envío de correo usando la función o servicio correspondiente
        # Por ejemplo: enviar_correo_token_sesion(email_usuario, sesion.token_anonimo)

        return jsonify({
            'success': True,
            'message': 'Token de sesión reenviado exitosamente'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al reenviar token: {str(e)}'
        }), 500
