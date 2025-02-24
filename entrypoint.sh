#!/bin/sh

# Check whether the database needs to be waited for
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#!/bin/sh

# Make sure that the SITE_DOMAIN variable is set
if [ -z "$SITE_DOMAIN" ]; then
    echo "Error: SITE_DOMAIN is not set"
    exit 1
fi

# Generate the configuration for Nginx
envsubst '$SITE_DOMAIN' < /var/www/$SITE_DOMAIN/nginx/default.nginx > /etc/nginx/sites-available/$SITE_DOMAIN

# Create a symbolic link in the sites-enabled
ln -sf /etc/nginx/sites-available/$SITE_DOMAIN /etc/nginx/sites-enabled/

# Let's reboot Nginx
systemctl reload nginx

# Start the main process
exec "$@"
