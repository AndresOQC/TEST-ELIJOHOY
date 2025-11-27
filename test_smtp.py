import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración desde .env.production
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'andresquilichechavez@gmail.com'
MAIL_PASSWORD = 'nlqxndgrpdotgqiy'

print("🔍 PRUEBA DE CONEXIÓN SMTP - GMAIL")
print("=" * 50)
print(f"Servidor: {MAIL_SERVER}:{MAIL_PORT}")
print(f"Usuario: {MAIL_USERNAME}")
print("=" * 50)

try:
    print("\n[1/3] Conectando a servidor SMTP...")
    server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=10)
    print("✅ Conexión exitosa")
    
    print("\n[2/3] Iniciando TLS...")
    server.starttls()
    print("✅ TLS iniciado")
    
    print("\n[3/3] Autenticando...")
    server.login(MAIL_USERNAME, MAIL_PASSWORD)
    print("✅ Autenticación exitosa")
    
    print("\n🎉 TODAS LAS PRUEBAS PASARON")
    print("\n💌 Enviando email de prueba...")
    
    msg = MIMEMultipart()
    msg['From'] = MAIL_USERNAME
    msg['To'] = MAIL_USERNAME
    msg['Subject'] = 'Test ElijHoy - Prueba SMTP'
    
    body = """
    Este es un email de prueba del sistema ElijHoy.
    
    Si recibes este mensaje, la configuración SMTP está correcta.
    
    Saludos,
    Sistema ElijHoy
    """
    
    msg.attach(MIMEText(body, 'plain'))
    server.send_message(msg)
    
    print(f"✅ Email enviado exitosamente a {MAIL_USERNAME}")
    
    server.quit()
    print("\n✅ Conexión cerrada")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n❌ ERROR DE AUTENTICACIÓN:")
    print(f"   {e}")
    print("\n💡 Soluciones:")
    print("   1. Verifica que la contraseña de aplicación sea correcta")
    print("   2. Genera una nueva en: https://myaccount.google.com/apppasswords")
    print("   3. Asegúrate de tener verificación en 2 pasos activada")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   {e}")
