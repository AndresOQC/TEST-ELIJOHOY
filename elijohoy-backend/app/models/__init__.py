from app.core.extensions import db
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol
from app.models.alumno import Alumno
from app.models.token import Token
from app.models.pregunta import Pregunta
from app.models.tipo_personalidad import TipoPersonalidad
from app.models.sesion_test import SesionTest
from app.models.respuesta import Respuesta

__all__ = [
    'db',
    'Usuario',
    'Rol',
    'UsuarioRol',
    'Alumno',
    'Token',
    'Pregunta',
    'TipoPersonalidad',
    'SesionTest',
    'Respuesta'
]