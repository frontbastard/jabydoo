#!/bin/bash

function deploy_nginx() {
  if [ "$(id -u)" != "0" ]; then
     echo "This script must be run as root" 1>&2
     exit 1
  fi

  # Determine the script directory (i.e., /var/www/site.com/nginx)
  SCRIPT_DIR="$(dirname "$(realpath "$0")")"

  # Determine the project root directory (one level up from SCRIPT_DIR)
  PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

  # Load variables from .env if the file exists
  ENV_FILE="$PROJECT_ROOT/.env"
  if [ -f "$ENV_FILE" ]; then
      export $(grep -v '^#' "$ENV_FILE" | xargs)
  fi

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
