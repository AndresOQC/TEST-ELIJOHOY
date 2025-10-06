"""Script para ejecutar migraciones en orden usando SQLAlchemy."""
import os
import sys
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Agregar el directorio actual al path para importar módulos
sys.path.append('.')

load_dotenv()

def run_migrations():
    """Ejecuta todas las migraciones en orden."""

    # Obtener URL de la base de datos
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: Variable de entorno DATABASE_URL no encontrada")
        return False

    print(f"🔗 Conectando a base de datos...")

    try:
        # Crear engine de SQLAlchemy
        engine = create_engine(database_url, echo=False)

        # Crear sesión
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

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
            '13_vistas_utiles.sql',
            '14_usuarios_prueba.sql'
        ]

        migrations_dir = 'migrations'
        executed_count = 0
        failed_count = 0

        print(f"📁 Ejecutando {len(migrations)} migraciones desde {migrations_dir}/")

        for migration_file in migrations:
            file_path = os.path.join(migrations_dir, migration_file)
            print(f"\n🔄 Ejecutando: {migration_file}...")

            try:
                # Verificar que el archivo existe
                if not os.path.exists(file_path):
                    print(f"❌ ERROR: Archivo {file_path} no encontrado")
                    failed_count += 1
                    continue

                # Leer el archivo SQL
                with open(file_path, 'r', encoding='utf-8') as f:
                    sql = f.read()

                # Verificar que no esté vacío
                if not sql.strip():
                    print(f"⚠️  ADVERTENCIA: Archivo {migration_file} está vacío")
                    continue

                # Ejecutar la migración
                session.execute(text(sql))
                session.commit()

                print(f"✅ [OK] {migration_file} ejecutada exitosamente")
                executed_count += 1

            except Exception as e:
                print(f"❌ [ERROR] Error en {migration_file}: {str(e)}")
                session.rollback()
                failed_count += 1

                # Mostrar más detalles del error si es posible
                if hasattr(e, 'orig'):
                    print(f"   Detalles: {e.orig}")
                if hasattr(e, 'statement'):
                    print(f"   SQL: {e.statement}")

                # Continuar con la siguiente migración
                continue

        # Cerrar sesión
        session.close()

        print(f"\n📊 Resumen de migraciones:")
        print(f"   ✅ Ejecutadas exitosamente: {executed_count}")
        print(f"   ❌ Fallidas: {failed_count}")
        print(f"   📁 Total: {len(migrations)}")

        if failed_count == 0:
            print("\n🎉 ¡Todas las migraciones se ejecutaron correctamente!")
            return True
        else:
            print(f"\n⚠️  {failed_count} migraciones fallaron. Revisa los errores arriba.")
            return False

    except Exception as e:
        print(f"❌ ERROR CRÍTICO al conectar a la base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
