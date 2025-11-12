from flask import current_app, render_template_string
from flask_mail import Message
from app.core.extensions import mail
import threading

def send_async_email(app, msg):
    """Enviar email de forma asíncrona."""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f'Error enviando email: {str(e)}')

def send_email(to, subject, template, **kwargs):
    """Enviar email."""
    try:
        msg = Message(
            subject=subject,
            recipients=[to],
            html=template,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        # Enviar de forma asíncrona
        app = current_app._get_current_object()
        thread = threading.Thread(target=send_async_email, args=[app, msg])
        thread.start()
        
        return True
    except Exception as e:
        current_app.logger.error(f'Error preparando email: {str(e)}')
        return False

def send_password_reset_email(user_email, user_name, reset_token):
    """Enviar email de recuperación de contraseña."""
    # Construir la URL de restablecimiento
    # La configuración debe ser la URL base del frontend (ej: https://www.elijohoy.com)
    base_url = current_app.config['PASSWORD_RESET_URL']
    
    # Si la URL base ya incluye la ruta completa, usarla directamente
    if '/auth/restablecer-password' in base_url:
        # El .env ya tiene la ruta completa, solo agregamos el token
        reset_url = f"{base_url}/{reset_token}"
    else:
        # El .env solo tiene el dominio, construimos la ruta completa
        if base_url.endswith('/'):
            reset_url = f"{base_url}#/auth/restablecer-password/{reset_token}"
        else:
            reset_url = f"{base_url}/#/auth/restablecer-password/{reset_token}"
    
    # Template HTML para el email
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recuperar Contraseña - ElijHoy</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }
            .content {
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }
            .button {
                display: inline-block;
                background: #fbbf24;
                color: #7c2d12;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 20px 0;
            }
            .warning {
                background: #fef3c7;
                border: 1px solid #f59e0b;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔐 Recuperar Contraseña</h1>
            <p>ElijHoy - Orientación Vocacional</p>
        </div>
        
        <div class="content">
            <h2>¡Hola {{ user_name }}!</h2>
            
            <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta en ElijHoy.</p>
            
            <p>Si fuiste tú quien solicitó este cambio, haz clic en el siguiente botón para crear una nueva contraseña:</p>
            
            <div style="text-align: center;">
                <a href="{{ reset_url }}" class="button">Restablecer Contraseña</a>
            </div>
            
            <div class="warning">
                <strong>⚠️ Importante:</strong>
                <ul>
                    <li>Este enlace expirará en <strong>1 hora</strong></li>
                    <li>Solo puede ser usado una vez</li>
                    <li>Si no solicitaste este cambio, ignora este email</li>
                </ul>
            </div>
            
            <p>Si el botón no funciona, puedes copiar y pegar este enlace en tu navegador:</p>
            <p style="background: #e5e7eb; padding: 10px; border-radius: 5px; word-break: break-all;">
                {{ reset_url }}
            </p>
            
            <p>Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.</p>
            
            <p>¡Gracias por usar ElijHoy! 🚀</p>
        </div>
        
        <div class="footer">
            <p>Este es un email automático, por favor no respondas a este mensaje.</p>
            <p>© 2025 ElijHoy - Orientación Vocacional</p>
        </div>
    </body>
    </html>
    """
    
    # Renderizar template con variables
    html_content = render_template_string(
        html_template, 
        user_name=user_name, 
        reset_url=reset_url
    )
    
    return send_email(
        to=user_email,
        subject='🔐 Recuperar Contraseña - ElijHoy',
        template=html_content
    )