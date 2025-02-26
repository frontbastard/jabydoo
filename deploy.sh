#!/bin/bash

# Loading variables from the .env file
source .env

# Ensure that SITE_DOMAIN is set
if [ -z "$SITE_DOMAIN" ]; then
    echo "Error: SITE_DOMAIN is not set in .env"
    exit 1
fi

# Import functions from deploy_nginx.sh
source ./nginx/deploy_nginx.sh

# Performing functions from deploy_nginx.sh
deploy_nginx

# Obtaining an SSL certificate
sudo certbot --nginx -d $SITE_DOMAIN -d www.$SITE_DOMAIN --non-interactive --agree-tos --email info@hornshooves.com

# Restart Nginx
sudo systemctl reload nginx

# Run Docker Compose
docker compose up --build -d

# Reload Nginx
systemctl reload nginx
