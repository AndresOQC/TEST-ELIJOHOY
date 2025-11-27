FROM nginx:alpine

# Instalar certbot para renovación de certificados
RUN apk add --no-cache certbot certbot-nginx

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY elijohoy.conf /etc/nginx/conf.d/elijohoy.conf

# Crear directorio para desafíos de Let's Encrypt
RUN mkdir -p /var/www/certbot

# Exponer puertos
EXPOSE 80 443

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
