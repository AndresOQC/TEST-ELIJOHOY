#!/bin/sh
set -e

echo "🟢 Entrypoint: esperando a la base de datos..."

# Esperar a que PostgreSQL esté listo
until PGPASSWORD="${POSTGRES_PASSWORD:-elijohoy_password}" psql -h db -U "${POSTGRES_USER:-elijohoy_user}" -d "${POSTGRES_DB:-elijohoy_db}" -c '\q' 2>/dev/null; do
  echo "⏳ Esperando a PostgreSQL..."
  sleep 2
done

echo "✅ PostgreSQL está listo!"

echo "🔁 Ejecutando migraciones (run_migrations.py)..."
python run_migrations.py || echo "⚠️  run_migrations devolvió error (continuando)"

if [ "$FLASK_ENV" = "production" ]; then
  echo "🚀 Iniciando gunicorn..."
  exec gunicorn -w 4 -b 0.0.0.0:${PORT:-5001} "app.core.app_factory:create_app()"
else
  echo "🐍 Iniciando Flask (development)..."
  exec python app.py
fi
