#!/bin/bash
set -e

echo "🚀 Desplegando ELIJOHOY en Contabo con Docker"
echo "============================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.prod.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.prod.yml no encontrado${NC}"
    echo "Por favor ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que existe el archivo .env.production
if [ ! -f ".env.production" ]; then
    echo -e "${RED}❌ Error: .env.production no encontrado en la raíz del proyecto${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Usando archivo: .env.production${NC}"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE: Verifica que .env.production tenga las credenciales correctas:${NC}"
echo "  1. SECRET_KEY - Debe ser único"
echo "  2. JWT_SECRET_KEY - Debe ser único"
echo "  3. POSTGRES_PASSWORD - Contraseña segura"
echo "  4. MAIL_USERNAME y MAIL_PASSWORD - Credenciales de email"
echo ""
read -p "¿Las credenciales en .env.production están correctas? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Edita .env.production y ejecuta este script nuevamente"
    exit 1
fi

echo ""
echo -e "${GREEN}1️⃣  Deteniendo servicios antiguos (PM2 y systemd)...${NC}"
sudo systemctl stop backend.service 2>/dev/null || echo "backend.service ya estaba detenido"
sudo systemctl disable backend.service 2>/dev/null || echo "backend.service no estaba habilitado"
pm2 stop elijohoy-frontend-dev 2>/dev/null || echo "PM2 frontend ya estaba detenido"
pm2 delete elijohoy-frontend-dev 2>/dev/null || echo "PM2 frontend ya estaba eliminado"
pm2 save 2>/dev/null || true

echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE: Verificando certificados SSL...${NC}"
if [ ! -d "/etc/letsencrypt/live/elijohoy.com" ]; then
    echo -e "${RED}❌ Error: Certificados SSL no encontrados en /etc/letsencrypt/live/elijohoy.com${NC}"
    echo "Por favor, obtén los certificados SSL primero con certbot antes de continuar."
    echo "Ejecuta: sudo certbot certonly --standalone -d elijohoy.com -d www.elijohoy.com"
    exit 1
else
    echo -e "${GREEN}✅ Certificados SSL encontrados${NC}"
    sudo certbot certificates
fi

# Crear directorios necesarios
mkdir -p nginx/logs
mkdir -p nginx/certbot

echo ""
echo -e "${YELLOW}📝 NOTA: Nginx de Docker usará puertos 8080 (HTTP) y 8443 (HTTPS)${NC}"
echo -e "${YELLOW}   Debes configurar tu Nginx existente para hacer proxy a estos puertos${NC}"

echo ""
echo -e "${GREEN}2️⃣  Deteniendo contenedores existentes (si hay)...${NC}"
docker compose -f docker-compose.prod.yml --env-file .env.production down 2>/dev/null || true

echo ""
echo -e "${GREEN}3️⃣  Construyendo imágenes Docker...${NC}"
docker compose -f docker-compose.prod.yml --env-file .env.production build --no-cache

echo ""
echo -e "${GREEN}4️⃣  Iniciando servicios con Docker Compose...${NC}"
docker compose -f docker-compose.prod.yml --env-file .env.production up -d

echo ""
echo -e "${GREEN}5️⃣  Esperando a que los servicios estén listos...${NC}"
sleep 10

echo ""
echo -e "${GREEN}6️⃣  Verificando estado de los contenedores...${NC}"
docker compose -f docker-compose.prod.yml ps

echo ""
echo -e "${GREEN}7️⃣  Verificando logs del backend...${NC}"
docker compose -f docker-compose.prod.yml logs backend | tail -n 20

echo ""
echo -e "${GREEN}8️⃣  Verificando logs de Nginx...${NC}"
docker compose -f docker-compose.prod.yml logs nginx | tail -n 20

echo ""
echo "============================================="
echo -e "${GREEN}✅ Despliegue completado!${NC}"
echo ""
echo "📊 Comandos útiles:"
echo "  - Ver logs en tiempo real:    docker compose -f docker-compose.prod.yml logs -f"
echo "  - Ver solo backend:            docker compose -f docker-compose.prod.yml logs -f backend"
echo "  - Ver solo frontend:           docker compose -f docker-compose.prod.yml logs -f frontend"
echo "  - Ver solo nginx:              docker compose -f docker-compose.prod.yml logs -f nginx"
echo "  - Reiniciar servicios:         docker compose -f docker-compose.prod.yml restart"
echo "  - Detener todo:                docker compose -f docker-compose.prod.yml down"
echo "  - Ver estado:                  docker compose -f docker-compose.prod.yml ps"
echo ""
echo "🌐 URLs Docker:"
echo "  - Nginx Docker HTTP:  http://tu-servidor:8080"
echo "  - Nginx Docker HTTPS: https://tu-servidor:8443"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE - Configuración del Nginx del Host:${NC}"
echo "  Ahora debes configurar tu Nginx EXISTENTE (/etc/nginx/sites-available/elijohoy)"
echo "  para hacer proxy al Nginx de Docker en los puertos 8080 y 8443"
echo ""
echo "  Edita: /etc/nginx/sites-available/elijohoy"
echo "  Y cambia:"
echo "    location / {"
echo "      proxy_pass https://localhost:8443;  # Nginx de Docker"
echo "    }"
echo ""
echo "  Luego: sudo nginx -t && sudo systemctl reload nginx"
