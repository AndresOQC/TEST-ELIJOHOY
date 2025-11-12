import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

# Configuración del email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'andresquilichechavez@gmail.com'
MAIL_PASSWORD = 'trjnrbmctucbzelf'
MAIL_DEFAULT_SENDER = 'andresquilichechavez@gmail.com'

def test_email_connection():
    """Probar la conexión SMTP y envío de email."""
    
    print("=" * 60)
    print("PRUEBA DE CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    print(f"\nServidor SMTP: {MAIL_SERVER}")
    print(f"Puerto: {MAIL_PORT}")
    print(f"Usuario: {MAIL_USERNAME}")
    print(f"Remitente: {MAIL_DEFAULT_SENDER}")
    print("\n" + "=" * 60)
    
    try:
        # 1. Probar conexión al servidor SMTP
        print("\n[1/4] Conectando al servidor SMTP...")
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=10)
        print("✅ Conexión establecida")
        
        # 2. Iniciar TLS
        print("\n[2/4] Iniciando TLS...")
        server.starttls()
        print("✅ TLS iniciado correctamente")
        
        # 3. Autenticación
        print("\n[3/4] Autenticando...")
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        print("✅ Autenticación exitosa")
        
        # 4. Enviar email de prueba
        print("\n[4/4] Enviando email de prueba...")
        
        # Pedir email de destino
        to_email = input("\nIngresa el email de destino para la prueba: ").strip()
        
        if not to_email:
            print("❌ Email de destino requerido")
            server.quit()
            return False
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🔐 Prueba de Email - ElijHoy'
        msg['From'] = MAIL_DEFAULT_SENDER
        msg['To'] = to_email
        
        # Contenido HTML del email
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
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
                .success-box {
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>✅ Prueba de Email Exitosa</h1>
                <p>ElijHoy - Sistema de Orientación Vocacional</p>
            </div>
            
            <div class="content">
                <h2>¡Excelente!</h2>
                
                <div class="success-box">
                    <strong>✓ La configuración de email está funcionando correctamente</strong>
                </div>
                
                <p>Este es un email de prueba enviado desde el sistema ElijHoy para verificar que:</p>
                
                <ul>
                    <li>✅ La conexión SMTP está configurada correctamente</li>
                    <li>✅ Las credenciales son válidas</li>
                    <li>✅ El servidor puede enviar emails</li>
                    <li>✅ Los emails llegan a su destino</li>
                </ul>
                
                <p><strong>Configuración utilizada:</strong></p>
                <ul>
                    <li>Servidor: smtp.gmail.com</li>
                    <li>Puerto: 587</li>
                    <li>TLS: Activado</li>
                </ul>
                
                <p>Si recibes este email, significa que el sistema de recuperación de contraseña debería funcionar correctamente.</p>
                
                <p style="margin-top: 30px;">
                    <em>Este es un email de prueba automático generado por el sistema ElijHoy.</em>
                </p>
            </div>
        </body>
        </html>
        """
        
        # Adjuntar contenido HTML
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Enviar email
        server.send_message(msg)
        print(f"✅ Email enviado exitosamente a: {to_email}")
        
        # Cerrar conexión
        server.quit()
        
        print("\n" + "=" * 60)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\nRevisa tu bandeja de entrada (y spam) en:", to_email)
        print("\nSi recibiste el email, la configuración está correcta.")
        print("Si no lo recibiste, revisa:")
        print("  - Carpeta de spam/correo no deseado")
        print("  - Que la contraseña de aplicación de Gmail sea correcta")
        print("  - Que la verificación en 2 pasos esté activada en Gmail")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ ERROR DE AUTENTICACIÓN")
        print(f"Las credenciales son incorrectas o la cuenta no permite el acceso.")
        print(f"Detalle: {e}")
        print("\nVerifica:")
        print("  1. Usuario y contraseña correctos")
        print("  2. Usar contraseña de aplicación (no la contraseña normal de Gmail)")
        print("  3. Verificación en 2 pasos activada en Gmail")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ ERROR SMTP")
        print(f"Detalle: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO")
        print(f"Tipo: {type(e).__name__}")
        print(f"Detalle: {e}")
        return False

if __name__ == "__main__":
    try:
        test_email_connection()
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba cancelada por el usuario")
        sys.exit(0)
