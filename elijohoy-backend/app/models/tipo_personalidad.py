from app.core.extensions import db

class TipoPersonalidad(db.Model):
    """Modelo para la tabla tipos_personalidad."""

    __tablename__ = 'tipos_personalidad'

    codigo = db.Column(db.String(4), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion_corta = db.Column(db.Text, nullable=False)
    descripcion_completa = db.Column(db.Text, nullable=False)
    fortalezas = db.Column(db.Text)
    debilidades = db.Column(db.Text)
    carreras_sugeridas = db.Column(db.Text)
    famosos_tipo = db.Column(db.Text)
    porcentaje_poblacion = db.Column(db.Numeric(4, 2))

    # Relaciones
    sesiones = db.relationship('SesionTest', back_populates='tipo', lazy='dynamic')

    def __repr__(self):
        return f'<TipoPersonalidad {self.codigo}: {self.nombre}>'

    def to_dict(self):
        """Convertir el objeto a diccionario."""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion_corta': self.descripcion_corta,
            'descripcion_completa': self.descripcion_completa,
            'fortalezas': self.fortalezas,
            'debilidades': self.debilidades,
            'carreras_sugeridas': self.carreras_sugeridas,
            'famosos_tipo': self.famosos_tipo,
            'porcentaje_poblacion': float(self.porcentaje_poblacion) if self.porcentaje_poblacion else None
        }
