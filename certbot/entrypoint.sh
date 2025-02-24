#!/bin/sh

# Directory for certificates
CERT_DIR="/etc/letsencrypt/live/$SITE_DOMAIN"

# If certificates are missing, get new ones
if [ ! -d "$CERT_DIR" ]; then
  echo "The certificates are missing. Run certbot..."
  certbot certonly --webroot -w /var/www/certbot -d $SITE_DOMAIN -d www.$SITE_DOMAIN \
    --email your@email.com --agree-tos --no-eff-email --force-renewal

  echo "Restarting Nginx..."
  docker compose restart nginx
else
  echo "The certificates already exist. Let's start the update..."
  certbot renew --quiet
fi

# Infinite loop to automatically renew certificates every 12 hours
while :; do
  certbot renew --quiet
  sleep 12h
done
