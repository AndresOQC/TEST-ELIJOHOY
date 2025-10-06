from app.core.extensions import db

class Pregunta(db.Model):
    """Modelo para la tabla preguntas."""

    __tablename__ = 'preguntas'

    id_pregunta = db.Column(db.Integer, primary_key=True)
    texto_izquierda = db.Column(db.String(200), nullable=False)
    texto_derecha = db.Column(db.String(200), nullable=False)
    dimension = db.Column(db.String(2), nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    orden = db.Column(db.Integer, unique=True, nullable=False)
    activa = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    respuestas = db.relationship('Respuesta', back_populates='pregunta', lazy='dynamic')

    def __repr__(self):
        return f'<Pregunta {self.id_pregunta}: {self.dimension}>'

    def to_dict(self):
        """Convertir el objeto a diccionario."""
        return {
            'id_pregunta': self.id_pregunta,
            'texto_izquierda': self.texto_izquierda,
            'texto_derecha': self.texto_derecha,
            'dimension': self.dimension,
            'peso': self.peso,
            'orden': self.orden,
            'activa': self.activa
        }
