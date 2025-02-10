#!/bin/bash

DOMAIN_NAME=$1

if [ -z "$DOMAIN_NAME" ]; then
    echo "Використання: $0 example.com"
    exit 1
fi

NGINX_CONF_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"
CONF_FILE="$NGINX_CONF_DIR/$DOMAIN_NAME"

# Створюємо конфігураційний файл
cat > "$CONF_FILE" <<EOF
server {
    listen 443 ssl http2;
    server_name $DOMAIN_NAME www.$DOMAIN_NAME;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    location / {
        proxy_pass http://unix:/var/www/django/app.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

server {
    listen 80;
    server_name $DOMAIN_NAME www.$DOMAIN_NAME;

    return 301 https://\$host\$request_uri;
}
EOF

# Створюємо символічне посилання в sites-enabled
ln -s "$CONF_FILE" "$NGINX_ENABLED_DIR/"

# Перевіряємо конфігурацію Nginx і перезапускаємо сервер
nginx -t && systemctl reload nginx

echo "Конфігурація для $DOMAIN_NAME створена і активована!"
