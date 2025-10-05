from app.core.extensions import db
from datetime import datetime

class Rol(db.Model):
    """Modelo para la tabla roles."""
    
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    usuarios = db.relationship('UsuarioRol', back_populates='rol', lazy='dynamic')
    
    def __repr__(self):
        return f'<Rol {self.nombre}>'
    
    def to_dict(self):
        """Convertir el objeto a diccionario."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'creado_en': self.creado_en.isoformat() if self.creado_en else None
        }