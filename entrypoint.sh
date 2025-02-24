#!/bin/sh

# Check whether the database needs to be waited for
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Check if the command is already in the autorun (crontab)
if ! crontab -l 2>/dev/null | grep -q "docker compose up -d"; then
    echo "Adding Docker Compose to autorun..."

    # Add a command to the crontab to autorun after reboot
    (crontab -l 2>/dev/null; echo "@reboot sleep 10 && cd $(pwd) && docker compose up -d") | crontab -

    echo "Autostart has been successfully configured!"
else
    echo "Autorun is already set up."
fi

# Start the standard container startup process
exec "$@"
