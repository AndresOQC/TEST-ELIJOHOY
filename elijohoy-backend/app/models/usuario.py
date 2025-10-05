from app.core.extensions import db
from datetime import datetime

class Usuario(db.Model):
    """Modelo para la tabla usuarios."""
    
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    email_verificado = db.Column(db.Boolean, default=True, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime)
    intentos_login_fallidos = db.Column(db.Integer, default=0)
    bloqueado_hasta = db.Column(db.DateTime)
    
    # Relaciones
    roles = db.relationship('UsuarioRol', back_populates='usuario', lazy='dynamic')
    alumno = db.relationship('Alumno', back_populates='usuario', uselist=False)
    tokens = db.relationship('Token', back_populates='usuario', lazy='dynamic')
    
    def __repr__(self):
        return f'<Usuario {self.email}>'
    
    def has_role(self, role_name):
        """Verificar si el usuario tiene un rol específico."""
        return any(ur.rol.nombre == role_name for ur in self.roles)
    
    def get_roles(self):
        """Obtener lista de nombres de roles del usuario."""
        return [ur.rol.nombre for ur in self.roles]
    
    def to_dict(self, include_roles=False):
        """Convertir el objeto a diccionario."""
        data = {
            'id': self.id,
            'email': self.email,
            'activo': self.activo,
            'email_verificado': self.email_verificado,
            'creado_en': self.creado_en.isoformat() if self.creado_en else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None,
            'ultimo_login': self.ultimo_login.isoformat() if self.ultimo_login else None,
            'intentos_login_fallidos': self.intentos_login_fallidos,
            'bloqueado_hasta': self.bloqueado_hasta.isoformat() if self.bloqueado_hasta else None
        }
        
        # Agregar datos del alumno si existe
        if self.alumno:
            data.update({
                'nombre': self.alumno.nombre,
                'apellidos': self.alumno.apellidos,
                'nombre_completo': f"{self.alumno.nombre} {self.alumno.apellidos}",
                'edad': self.alumno.edad,
                'genero': self.alumno.genero,
                'ciudad': self.alumno.ciudad,
                'pais': self.alumno.pais,
                'institucion_educativa': self.alumno.institucion_educativa,
                'grado': self.alumno.grado,
                'seccion': self.alumno.seccion,
                'turno': self.alumno.turno
            })
        
        if include_roles:
            data['roles'] = self.get_roles()
            
        return data