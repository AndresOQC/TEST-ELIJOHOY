from app.core.extensions import db
from datetime import datetime

class UsuarioRol(db.Model):
    """Modelo para la tabla usuario_rol (many-to-many)."""
    
    __tablename__ = 'usuario_rol'
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, primary_key=True)
    asignado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='roles')
    rol = db.relationship('Rol', back_populates='usuarios')
    
    def __repr__(self):
        return f'<UsuarioRol usuario_id={self.usuario_id} rol_id={self.rol_id}>'
    
    def to_dict(self):
        """Convertir el objeto a diccionario."""
        return {
            'usuario_id': self.usuario_id,
            'rol_id': self.rol_id,
            'asignado_en': self.asignado_en.isoformat() if self.asignado_en else None,
            'rol': self.rol.to_dict() if self.rol else None,
            'usuario': self.usuario.to_dict() if self.usuario else None
        }