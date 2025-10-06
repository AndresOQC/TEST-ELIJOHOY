"""Script para ejecutar migraciones en orden."""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Obtener URL de la base de datos
database_url = os.getenv('DATABASE_URL')

# Parsear la URL
# postgresql://elijohoy_user:elijohoy_password@localhost:5432/elijhoy_db
parts = database_url.replace('postgresql://', '').split('@')
user_pass = parts[0].split(':')
host_db = parts[1].split('/')

user = user_pass[0]
password = user_pass[1]
host_port = host_db[0].split(':')
host = host_port[0]
port = host_port[1] if len(host_port) > 1 else '5432'
database = host_db[1]

print(f"Conectando a base de datos: {database}")

# Conectar
conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

cursor = conn.cursor()

# Lista de migraciones en orden
migrations = [
    '01_roles.sql',
    '02_usuarios.sql',
    '03_alumnos.sql',
    '04_usuario_rol.sql',
    '05_tokens.sql',
    '06_preguntas.sql',
    '07_tipos_personalidad.sql',
    '08_sesiones_test.sql',
    '09_respuestas.sql',
    '10_datos_iniciales_preguntas.sql',
    '11_datos_iniciales_tipos.sql',
    '12_funciones_almacenadas.sql',
    '13_vistas_utiles.sql'
]

migrations_dir = 'migrations'

for migration_file in migrations:
    file_path = os.path.join(migrations_dir, migration_file)
    print(f"\nEjecutando: {migration_file}...")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql = f.read()

        cursor.execute(sql)
        conn.commit()
        print(f"[OK] {migration_file} ejecutada exitosamente")
    except Exception as e:
        print(f"[ERROR] Error en {migration_file}: {str(e)}")
        conn.rollback()
        # Continuar con la siguiente migración

cursor.close()
conn.close()

print("\n¡Migraciones completadas!")
