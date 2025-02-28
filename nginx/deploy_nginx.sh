#!/bin/bash

function deploy_nginx() {
  # Determine the script directory (i.e., /var/www/site.com/nginx)
  SCRIPT_DIR="$(dirname "$(realpath "$0")")"

  # Generate the Nginx configuration
  envsubst '$SITE_DOMAIN' < "$SCRIPT_DIR/default.nginx" > "/etc/nginx/sites-available/$SITE_DOMAIN"

  # Create a symbolic link
  ln -sf "/etc/nginx/sites-available/$SITE_DOMAIN" "/etc/nginx/sites-enabled/"

  # Verify that everything is working
  echo "🔹 Nginx configs in sites-available:"
  ls -la /etc/nginx/sites-available/
  echo "🔹 Nginx configs in sites-enabled:"
  ls -la /etc/nginx/sites-enabled/

  echo "✅ Nginx configuration for $SITE_DOMAIN has been updated and activated!"
}
