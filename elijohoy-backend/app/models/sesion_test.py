from app.core.extensions import db
from datetime import datetime

class SesionTest(db.Model):
    """Modelo para la tabla sesiones_test."""

    __tablename__ = 'sesiones_test'

    id_sesion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    token_anonimo = db.Column(db.String(64), unique=True)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_fin = db.Column(db.DateTime)
    completado = db.Column(db.Boolean, default=False, nullable=False)
    resultado_ie = db.Column(db.Integer)
    resultado_sn = db.Column(db.Integer)
    resultado_ft = db.Column(db.Integer)
    resultado_jp = db.Column(db.Integer)
    tipo_personalidad = db.Column(db.String(4), db.ForeignKey('tipos_personalidad.codigo'))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)

    # Relaciones
    usuario = db.relationship('Usuario', backref=db.backref('sesiones_test', lazy='dynamic'))
    tipo = db.relationship('TipoPersonalidad', back_populates='sesiones')
    respuestas = db.relationship('Respuesta', back_populates='sesion', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<SesionTest {self.id_sesion}>'

    def to_dict(self, include_respuestas=False, include_tipo=False, include_usuario=False):
        """Convertir el objeto a diccionario."""
        data = {
            'id_sesion': self.id_sesion,
            'id_usuario': self.id_usuario,
            'token_anonimo': self.token_anonimo,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'completado': self.completado,
            'resultado_ie': self.resultado_ie,
            'resultado_sn': self.resultado_sn,
            'resultado_ft': self.resultado_ft,
            'resultado_jp': self.resultado_jp,
            'tipo_personalidad': self.tipo_personalidad,
            'ip_address': self.ip_address
        }

        if include_respuestas:
            data['respuestas'] = [r.to_dict() for r in self.respuestas]

        if include_tipo and self.tipo:
            data['tipo'] = self.tipo.to_dict()

        if include_usuario and self.usuario and self.usuario.alumno:
            data['usuario'] = {
                'id': self.usuario.id,
                'email': self.usuario.email,
                'nombre': self.usuario.alumno.nombre,
                'apellidos': self.usuario.alumno.apellidos,
                'edad': self.usuario.alumno.edad,
                'genero': self.usuario.alumno.genero,
                'ciudad': self.usuario.alumno.ciudad,
                'pais': self.usuario.alumno.pais,
                'institucion_educativa': self.usuario.alumno.institucion_educativa,
                'grado': self.usuario.alumno.grado,
                'seccion': self.usuario.alumno.seccion,
                'turno': self.usuario.alumno.turno
            }

        return data

    def contar_respuestas(self):
        """Contar el número de respuestas de esta sesión."""
        return self.respuestas.count()

    def esta_completa(self):
        """Verificar si la sesión tiene las 32 respuestas."""
        return self.contar_respuestas() == 32
