from app.core.extensions import db
from datetime import datetime

class Respuesta(db.Model):
    """Modelo para la tabla respuestas."""

    __tablename__ = 'respuestas'

    id_respuesta = db.Column(db.Integer, primary_key=True)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesiones_test.id_sesion'), nullable=False)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.id_pregunta'), nullable=False)
    valor_respuesta = db.Column(db.Integer, nullable=False)
    tiempo_respuesta = db.Column(db.Integer)
    fecha_respuesta = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    sesion = db.relationship('SesionTest', back_populates='respuestas')
    pregunta = db.relationship('Pregunta', back_populates='respuestas')

    # Constraint única para sesión + pregunta
    __table_args__ = (
        db.UniqueConstraint('id_sesion', 'id_pregunta', name='uk_sesion_pregunta'),
    )

    def __repr__(self):
        return f'<Respuesta Sesión={self.id_sesion} Pregunta={self.id_pregunta}>'

    def to_dict(self, include_pregunta=False):
        """Convertir el objeto a diccionario."""
        data = {
            'id_respuesta': self.id_respuesta,
            'id_sesion': self.id_sesion,
            'id_pregunta': self.id_pregunta,
            'valor_respuesta': self.valor_respuesta,
            'tiempo_respuesta': self.tiempo_respuesta,
            'fecha_respuesta': self.fecha_respuesta.isoformat() if self.fecha_respuesta else None
        }

        if include_pregunta and self.pregunta:
            data['pregunta'] = self.pregunta.to_dict()

        return data
