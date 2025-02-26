#!/bin/bash

# Check whether the database needs to be waited for
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Continue with the rest of the entrypoint process
exec "$@"
