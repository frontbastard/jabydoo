#!/bin/bash

# ======== Settings =========
EMAIL="admin@yourdomain.com"
AUTO_RENEW=true

# ======== Functions =========

# 1. Check if certbot is installed
if ! command -v certbot &> /dev/null; then
    echo "🔹 Installing Certbot..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
else
    echo "✅ Certbot is already installed!"
fi

# 2. Obtaining certificates
echo "🔹 Obtaining SSL certificates for all domains in Nginx..."
sudo certbot --nginx -n --agree-tos --email "$EMAIL" --no-eff-email --redirect

# 3. Automatic update (via cron)
if [ "$AUTO_RENEW" = true ]; then
    echo "🔹 Set up automatic certificate updates..."
    (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet") | crontab -
fi

echo "✅ Certificates successfully configured! 🎉"
