from app.core.extensions import db
from datetime import datetime

class Token(db.Model):
    """Modelo para la tabla tokens (gestión de JWT)."""
    
    __tablename__ = 'tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    jti = db.Column(db.String(120), nullable=False, unique=True, index=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'access' o 'refresh'
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_expiracion = db.Column(db.DateTime, nullable=False)
    revocado = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='tokens')
    
    def __repr__(self):
        return f'<Token {self.jti} tipo={self.tipo}>'
    
    @classmethod
    def create_password_reset_token(cls, usuario_id, expires_in_seconds=3600):
        """Crear un token de recuperación de contraseña."""
        import secrets
        from datetime import timedelta
        
        # Revocar tokens de recuperación anteriores del usuario
        cls.query.filter_by(
            usuario_id=usuario_id, 
            tipo='password_reset', 
            revocado=False
        ).update({'revocado': True})
        
        # Crear nuevo token
        token = cls(
            usuario_id=usuario_id,
            jti=secrets.token_urlsafe(32),
            tipo='password_reset',
            fecha_expiracion=datetime.utcnow() + timedelta(seconds=expires_in_seconds)
        )
        
        db.session.add(token)
        db.session.commit()
        return token
    
    @classmethod
    def verify_password_reset_token(cls, jti):
        """Verificar y obtener token de recuperación válido."""
        token = cls.query.filter_by(
            jti=jti, 
            tipo='password_reset', 
            revocado=False
        ).first()
        
        if not token:
            return None
        
        if datetime.utcnow() > token.fecha_expiracion:
            return None
        
        return token
    
    @classmethod
    def revoke_token(cls, jti):
        """Revocar un token específico."""
        token = cls.query.filter_by(jti=jti).first()
        if token:
            token.revocado = True
            db.session.commit()
            return True
        return False
    
    @classmethod
    def is_token_revoked(cls, jti):
        """Verificar si un token está revocado."""
        token = cls.query.filter_by(jti=jti).first()
        return token is None or token.revocado
    
    def use_token(self):
        """Marcar el token como usado (revocado)."""
        self.revocado = True
        db.session.commit()
    
    def is_expired(self):
        """Verificar si el token ha expirado."""
        return datetime.utcnow() > self.fecha_expiracion
    
    def to_dict(self):
        """Convertir el objeto a diccionario."""
        return {
            'id': self.id,
            'jti': self.jti,
            'usuario_id': self.usuario_id,
            'tipo': self.tipo,
            'revocado': self.revocado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_expiracion': self.fecha_expiracion.isoformat() if self.fecha_expiracion else None
        }