from app.core.extensions import db
from datetime import datetime

class Alumno(db.Model):
    """Modelo para la tabla alumnos."""
    
    __tablename__ = 'alumnos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    ciudad = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    institucion_educativa = db.Column(db.String(200))
    grado = db.Column(db.String(50))
    seccion = db.Column(db.String(50))
    turno = db.Column(db.String(50))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='alumno')
    
    def __repr__(self):
        return f'<Alumno {self.nombre} {self.apellidos}>'
    
    def to_dict(self, include_usuario=False):
        """Convertir el objeto a diccionario."""
        data = {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'nombre_completo': f"{self.nombre} {self.apellidos}",
            'edad': self.edad,
            'genero': self.genero,
            'email': self.email,
            'ciudad': self.ciudad,
            'pais': self.pais,
            'institucion_educativa': self.institucion_educativa,
            'grado': self.grado,
            'seccion': self.seccion,
            'turno': self.turno,
            'creado_en': self.creado_en.isoformat() if self.creado_en else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None
        }
        
        if include_usuario and self.usuario:
            data['usuario'] = self.usuario.to_dict()
            
        return data