from email_validator import validate_email, EmailNotValidError
import re

def validate_user_data(data, is_registration=False):
    """Validar datos de usuario."""
    errors = []
    
    # Validar email
    if 'email' in data:
        try:
            # Normalizar y validar email
            validated_email = validate_email(data['email'])
            data['email'] = validated_email.email
        except EmailNotValidError:
            errors.append('Email no válido')
    elif is_registration:
        errors.append('Email es requerido')
    
    # Validar password
    if 'password' in data:
        password = data['password']
        if len(password) < 8:
            errors.append('Password debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', password):
            errors.append('Password debe contener al menos una mayúscula')
        if not re.search(r'[a-z]', password):
            errors.append('Password debe contener al menos una minúscula')
        if not re.search(r'\d', password):
            errors.append('Password debe contener al menos un número')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('Password debe contener al menos un carácter especial')
    elif is_registration:
        errors.append('Password es requerido')
    
    # Validar nombre (solo en registro)
    if is_registration:
        if not data.get('nombre') or len(data['nombre'].strip()) < 2:
            errors.append('Nombre es requerido y debe tener al menos 2 caracteres')
        if not data.get('apellidos') or len(data['apellidos'].strip()) < 2:
            errors.append('Apellidos son requeridos y deben tener al menos 2 caracteres')
    
    # Validar edad (opcional)
    if 'edad' in data and data['edad'] is not None:
        try:
            edad = int(data['edad'])
            if edad < 13 or edad > 120:
                errors.append('Edad debe estar entre 13 y 120 años')
        except (ValueError, TypeError):
            errors.append('Edad debe ser un número válido')
    
    # Validar género (opcional)
    if 'genero' in data and data['genero']:
        valid_genders = ['masculino', 'femenino', 'otro', 'prefiero no decir']
        if data['genero'].lower() not in valid_genders:
            errors.append('Género debe ser: Masculino, Femenino, Otro, o Prefiero no decir')
    
    return errors

def sanitize_string(value, max_length=None):
    """Sanitizar strings."""
    if not value:
        return value
    
    # Limpiar espacios extra
    cleaned = ' '.join(value.strip().split())
    
    # Truncar si es necesario
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length].strip()
    
    return cleaned

def validate_pagination_params(page, per_page, max_per_page=100):
    """Validar parámetros de paginación."""
    try:
        page = int(page) if page else 1
        per_page = int(per_page) if per_page else 20
        
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 1
        if per_page > max_per_page:
            per_page = max_per_page
            
        return page, per_page, None
    except ValueError:
        return 1, 20, 'Parámetros de paginación inválidos'