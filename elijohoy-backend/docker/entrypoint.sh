#!/bin/sh
set -e

echo "🟢 Entrypoint: esperando a la base de datos..."

# Simple wait-for-postgres loop
until apk --no-cache --version >/dev/null 2>&1 || true; do break; done

RET=1
while [ $RET -ne 0 ]; do
  echo "Comprobando conexión a ${DATABASE_URL:-$DATABASE_URL}"
  python - <<PYCODE
import os, sys, time
from sqlalchemy import create_engine
url = os.environ.get('DATABASE_URL')
if not url:
    sys.exit(1)
try:
    engine = create_engine(url)
    conn = engine.connect()
    conn.close()
    sys.exit(0)
except Exception as e:
    print('DB no lista aún:', e)
    time.sleep(2)
    sys.exit(1)
PYCODE
  RET=$?
  if [ $RET -ne 0 ]; then
    sleep 2
  fi
done

echo "🔁 Ejecutando migraciones (run_migrations.py)..."
python run_migrations.py || echo "⚠️  run_migrations devolvió error (continuando)"

if [ "$FLASK_ENV" = "production" ]; then
  echo "🚀 Iniciando gunicorn..."
  exec gunicorn -w 4 -b 0.0.0.0:${PORT:-5001} app:app
else
  echo "🐍 Iniciando Flask (development)..."
  exec python app.py
fi
