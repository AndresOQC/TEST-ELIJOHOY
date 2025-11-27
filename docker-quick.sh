#!/bin/bash
# Comandos rápidos para gestionar ELIJOHOY en Docker
# Uso: ./docker-quick.sh [comando]

COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"

case "$1" in
  start)
    echo "🚀 Iniciando servicios..."
    docker compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
    ;;
    
  stop)
    echo "🛑 Deteniendo servicios..."
    docker compose -f $COMPOSE_FILE down
    ;;
    
  restart)
    echo "🔄 Reiniciando servicios..."
    docker compose -f $COMPOSE_FILE restart
    ;;
    
  status)
    echo "📊 Estado de los contenedores:"
    docker compose -f $COMPOSE_FILE ps
    ;;
    
  logs)
    if [ -z "$2" ]; then
      echo "📜 Mostrando logs de todos los servicios..."
      docker compose -f $COMPOSE_FILE logs -f --tail=100
    else
      echo "📜 Mostrando logs de $2..."
      docker compose -f $COMPOSE_FILE logs -f --tail=100 $2
    fi
    ;;
    
  rebuild)
    SERVICE=${2:-}
    if [ -z "$SERVICE" ]; then
      echo "🔨 Rebuilding todos los servicios..."
      docker compose -f $COMPOSE_FILE --env-file $ENV_FILE down
      docker compose -f $COMPOSE_FILE --env-file $ENV_FILE build --no-cache
      docker compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
    else
      echo "🔨 Rebuilding $SERVICE..."
      docker compose -f $COMPOSE_FILE stop $SERVICE
      docker compose -f $COMPOSE_FILE --env-file $ENV_FILE build --no-cache $SERVICE
      docker compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d $SERVICE
    fi
    ;;
    
  shell)
    SERVICE=${2:-backend}
    echo "🐚 Abriendo shell en $SERVICE..."
    if [ "$SERVICE" = "db" ]; then
      docker exec -it elijohoy_db_prod psql -U elijohoy_user -d elijohoy_db
    elif [ "$SERVICE" = "backend" ]; then
      docker exec -it elijohoy_backend_prod /bin/bash
    elif [ "$SERVICE" = "frontend" ]; then
      docker exec -it elijohoy_frontend_prod /bin/sh
    else
      echo "❌ Servicio no reconocido. Usa: backend, frontend, o db"
    fi
    ;;
    
  clean)
    echo "🧹 Limpiando contenedores detenidos, imágenes sin usar y cachés..."
    docker system prune -af --volumes
    ;;
    
  backup-db)
    BACKUP_DIR="./backups"
    mkdir -p $BACKUP_DIR
    BACKUP_FILE="$BACKUP_DIR/elijohoy_db_$(date +%Y%m%d_%H%M%S).sql"
    echo "💾 Creando backup de la base de datos..."
    docker exec elijohoy_db_prod pg_dump -U elijohoy_user elijohoy_db > $BACKUP_FILE
    echo "✅ Backup creado: $BACKUP_FILE"
    ;;
    
  restore-db)
    if [ -z "$2" ]; then
      echo "❌ Uso: ./docker-quick.sh restore-db <archivo.sql>"
      exit 1
    fi
    echo "⚠️  ADVERTENCIA: Esto sobrescribirá la base de datos actual"
    read -p "¿Continuar? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      echo "📥 Restaurando backup..."
      docker exec -i elijohoy_db_prod psql -U elijohoy_user elijohoy_db < $2
      echo "✅ Backup restaurado"
    fi
    ;;
    
  stats)
    echo "📈 Uso de recursos:"
    docker stats --no-stream
    ;;
    
  update)
    echo "🔄 Actualizando desde Git y rebuilding..."
    git pull
    docker compose -f $COMPOSE_FILE --env-file $ENV_FILE down
    docker compose -f $COMPOSE_FILE --env-file $ENV_FILE build --no-cache
    docker compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
    echo "✅ Actualización completada"
    ;;
    
  health)
    echo "🏥 Verificando salud de los servicios..."
    echo ""
    echo "Backend API:"
    curl -s http://127.0.0.1:5001/api/health | python3 -m json.tool || echo "❌ Backend no responde"
    echo ""
    echo "Frontend:"
    curl -s -o /dev/null -w "Status: %{http_code}\n" http://185.111.156.248:9000 || echo "❌ Frontend no responde"
    echo ""
    echo "PostgreSQL:"
    docker exec elijohoy_db_prod pg_isready -U elijohoy_user || echo "❌ PostgreSQL no responde"
    ;;
    
  *)
    echo "🐳 ELIJOHOY - Comandos Docker Rápidos"
    echo ""
    echo "Uso: ./docker-quick.sh [comando] [opciones]"
    echo ""
    echo "Comandos disponibles:"
    echo "  start           - Iniciar todos los servicios"
    echo "  stop            - Detener todos los servicios"
    echo "  restart         - Reiniciar todos los servicios"
    echo "  status          - Ver estado de los contenedores"
    echo "  logs [service]  - Ver logs (opcional: backend, frontend, db)"
    echo "  rebuild [serv]  - Reconstruir contenedores (opcional: especificar servicio)"
    echo "  shell [service] - Abrir shell (backend, frontend, o db)"
    echo "  clean           - Limpiar contenedores y cachés"
    echo "  backup-db       - Crear backup de PostgreSQL"
    echo "  restore-db <f>  - Restaurar backup de PostgreSQL"
    echo "  stats           - Ver uso de recursos"
    echo "  update          - Git pull y rebuild"
    echo "  health          - Verificar salud de servicios"
    echo ""
    echo "Ejemplos:"
    echo "  ./docker-quick.sh start"
    echo "  ./docker-quick.sh logs backend"
    echo "  ./docker-quick.sh rebuild frontend"
    echo "  ./docker-quick.sh shell db"
    ;;
esac
