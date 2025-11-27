# Instalación de Nginx Host como Proxy Inverso

Este archivo configura el Nginx del host (puerto 80/443) para que actúe como proxy inverso hacia el contenedor Docker Nginx (puerto 8443).

## Pasos de Instalación en Contabo

### 1. Copiar el archivo de configuración al servidor

```bash
# Desde tu máquina local (Windows)
scp nginx-host-config/elijohoy.com.conf root@185.111.156.248:/etc/nginx/sites-available/elijohoy.com

# O manualmente en el servidor, crear el archivo:
nano /etc/nginx/sites-available/elijohoy.com
# Pega el contenido de elijohoy.com.conf
```

### 2. Desactivar configuración anterior (si existe)

```bash
# Ver configuraciones activas
ls -la /etc/nginx/sites-enabled/

# Desactivar configuración anterior de elijohoy (si existe)
rm /etc/nginx/sites-enabled/elijohoy
rm /etc/nginx/sites-enabled/elijohoy.com  # si ya existía
```

### 3. Activar la nueva configuración

```bash
# Crear symlink en sites-enabled
ln -s /etc/nginx/sites-available/elijohoy.com /etc/nginx/sites-enabled/elijohoy.com

# Verificar que el symlink se creó correctamente
ls -la /etc/nginx/sites-enabled/ | grep elijohoy
```

### 4. Verificar la configuración de Nginx

```bash
# Probar la configuración
nginx -t

# Deberías ver:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 5. Recargar Nginx

```bash
# Recargar configuración sin downtime
systemctl reload nginx

# O reiniciar completamente
systemctl restart nginx

# Verificar estado
systemctl status nginx
```

### 6. Verificar que funciona

```bash
# Probar desde el servidor
curl -I http://localhost
curl -I https://localhost

# Probar desde fuera
curl -I http://elijohoy.com
curl -I https://elijohoy.com
```

## Arquitectura Final

```
Internet (puerto 80/443)
    ↓
Nginx HOST (185.111.156.248:80/443)
    ↓ proxy_pass https://127.0.0.1:8443
Docker Nginx Container (localhost:8443)
    ↓ proxy_pass http://frontend:9000
Frontend Container (Quasar Dev Server)
    
Docker Nginx Container (localhost:8443)
    ↓ proxy_pass http://backend:5001/api
Backend Container (Flask/Gunicorn)
```

## Troubleshooting

### Error: "nginx: [emerg] bind() to 0.0.0.0:80 failed"
Hay otro proceso usando el puerto 80:
```bash
netstat -tlnp | grep :80
# Detén el proceso que esté usando el puerto
```

### Error: "502 Bad Gateway"
El contenedor Docker no está corriendo:
```bash
cd ~/elijohoy
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs nginx
```

### Error: "SSL certificate problem"
Verifica que los certificados existan:
```bash
ls -la /etc/letsencrypt/live/elijohoy.com/
```

### Ver logs de Nginx
```bash
# Logs del Nginx host
tail -f /var/log/nginx/elijohoy.com.access.log
tail -f /var/log/nginx/elijohoy.com.error.log

# Logs del Nginx Docker
docker compose -f docker-compose.prod.yml logs -f nginx
```

## Renovación de Certificados SSL

Los certificados se renuevan automáticamente con certbot. Para verificar:

```bash
# Ver cuándo expiran
certbot certificates

# Renovar manualmente (si es necesario)
certbot renew

# Recargar Nginx después de renovar
systemctl reload nginx
```
