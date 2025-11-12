# 🐳 ElijHoy - Docker Setup

Sistema completo de orientación vocacional corriendo en contenedores Docker.

## 📋 Requisitos Previos

- Docker instalado
- Docker Compose instalado
- Git (para clonar el repositorio)

## 🚀 Inicio Rápido

### Modo Desarrollo (con hot-reload)

```bash
# Desde la raíz del proyecto
docker-compose up --build
```

Esto levantará:
- **Base de datos PostgreSQL**: `localhost:5433`
- **Backend Flask**: `http://localhost:5001`
- **Frontend Quasar**: `http://localhost:9000`

### Modo Producción

```bash
# Desde la raíz del proyecto
docker-compose -f docker-compose.prod.yml up --build
```

Esto levantará:
- **Base de datos PostgreSQL**: `localhost:5433`
- **Backend Flask** (con Gunicorn): `http://localhost:5001`
- **Frontend Quasar** (con Nginx): `http://localhost:80`

## 📁 Estructura de Archivos Docker

```
TEST-ELIJOHOY/
├── docker-compose.yml          # Configuración para desarrollo
├── docker-compose.prod.yml     # Configuración para producción
├── elijohoy-backend/
│   ├── Dockerfile              # Imagen del backend
│   ├── docker-compose.db.yml   # Solo base de datos
│   └── docker/
│       └── entrypoint.sh       # Script de inicio del backend
└── elijohoy-fronted/
    ├── Dockerfile              # Imagen de producción (Nginx)
    ├── Dockerfile.dev          # Imagen de desarrollo (hot-reload)
    └── nginx.conf              # Configuración de Nginx
```

## 🛠️ Comandos Útiles

### Ver logs en tiempo real
```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Solo base de datos
docker-compose logs -f db
```

### Detener los contenedores
```bash
# Detener sin eliminar
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener, eliminar contenedores y volúmenes (⚠️ ELIMINA LA BASE DE DATOS)
docker-compose down -v
```

### Reconstruir un servicio específico
```bash
# Reconstruir backend
docker-compose up --build backend

# Reconstruir frontend
docker-compose up --build frontend
```

### Ejecutar comandos dentro de los contenedores
```bash
# Acceder al backend
docker exec -it elijhoy_backend bash

# Acceder a la base de datos
docker exec -it elijhoy_db psql -U elijohoy_user -d elijohoy_db

# Ejecutar migraciones manualmente
docker exec -it elijhoy_backend python run_migrations.py
```

### Reiniciar un servicio
```bash
docker-compose restart backend
docker-compose restart frontend
docker-compose restart db
```

## 🔧 Configuración Personalizada

### Variables de Entorno

Las variables de entorno están definidas en el `docker-compose.yml`. Para personalizarlas:

1. **Backend** (Flask):
   - `FLASK_ENV`: `development` o `production`
   - `SECRET_KEY`: Clave secreta para Flask
   - `JWT_SECRET_KEY`: Clave para tokens JWT
   - `DATABASE_URL`: URL de conexión a PostgreSQL
   - `FRONTEND_URL`: URL del frontend
   - `SMTP_*`: Configuración de email (opcional)

2. **Base de Datos** (PostgreSQL):
   - `POSTGRES_USER`: Usuario de la base de datos
   - `POSTGRES_PASSWORD`: Contraseña de la base de datos
   - `POSTGRES_DB`: Nombre de la base de datos

### Puertos Personalizados

Para cambiar los puertos, edita el `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "PUERTO_EXTERNO:5001"  # Cambiar PUERTO_EXTERNO
  
  frontend:
    ports:
      - "PUERTO_EXTERNO:9000"  # Cambiar PUERTO_EXTERNO
```

## 🐛 Solución de Problemas

### El contenedor no inicia
```bash
# Ver logs detallados
docker-compose logs backend
docker-compose logs frontend
```

### Error de permisos en Linux/Mac
```bash
# Dar permisos al script de entrada
chmod +x elijohoy-backend/docker/entrypoint.sh
```

### La base de datos no se conecta
```bash
# Verificar que la base de datos esté corriendo
docker-compose ps

# Ver logs de la base de datos
docker-compose logs db

# Verificar conectividad
docker exec -it elijhoy_backend ping db
```

### Limpiar todo y empezar de nuevo
```bash
# ⚠️ ADVERTENCIA: Esto eliminará todos los datos
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Hot-reload no funciona en el frontend
Si estás en Windows con WSL, asegúrate de que el proyecto esté en el sistema de archivos de WSL, no en `/mnt/c/`.

## 📊 Monitoreo

### Ver recursos utilizados
```bash
docker stats
```

### Ver contenedores corriendo
```bash
docker-compose ps
```

### Inspeccionar un contenedor
```bash
docker inspect elijhoy_backend
docker inspect elijhoy_frontend
docker inspect elijhoy_db
```

## 🔐 Seguridad en Producción

Antes de deployar a producción:

1. **Cambiar las claves secretas**:
   - Genera nuevas claves para `SECRET_KEY` y `JWT_SECRET_KEY`
   - Usa variables de entorno o archivos `.env` seguros

2. **Configurar HTTPS**:
   - Agrega un reverse proxy (Nginx/Traefik) con certificados SSL
   - Usa Let's Encrypt para certificados gratuitos

3. **Configurar SMTP**:
   - Descomentar y configurar las variables `SMTP_*` en el `docker-compose.prod.yml`

4. **Base de datos**:
   - Usa una contraseña fuerte para `POSTGRES_PASSWORD`
   - Considera usar un servicio de base de datos administrado

## 📝 Notas Adicionales

- **Hot-reload**: En modo desarrollo, los cambios en el código se reflejan automáticamente
- **Volúmenes**: Los datos de la base de datos persisten en un volumen Docker
- **Networking**: Los servicios se comunican entre sí a través de la red `elijohoy_network`
- **Migraciones**: Se ejecutan automáticamente al iniciar el backend

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs: `docker-compose logs -f`
2. Verifica que los puertos no estén en uso
3. Asegúrate de tener la última versión de Docker
4. Prueba reconstruir: `docker-compose up --build --force-recreate`

---

**Desarrollado con ❤️ por AndresOQC**
