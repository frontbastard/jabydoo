#!/bin/bash

ENV_FILE="/var/www/django/.env"
SAMPLE_FILE="/var/www/django/.env.sample"
CREDENTIALS_FILE="$HOME/.password_credentials"

# 1. If .env does not already exist, create it from passwords
if [ ! -f "$ENV_FILE" ]; then
    cp "$CREDENTIALS_FILE" "$ENV_FILE"
    echo "Created $ENV_FILE з $CREDENTIALS_FILE"
fi

# 2. Add variables from .env.sample that are not yet defined in .env
while IFS= read -r line || [ -n "$line" ]; do
    # Skip blank lines and comments
    if [[ -z "$line" || "$line" == \#* ]]; then
        continue
    fi

    # Get the name of the variable (before the first =)
    VAR_NAME=$(echo "$line" | cut -d '=' -f1)

    # Check if this variable already exists in .env
    if ! grep -q "^$VAR_NAME=" "$ENV_FILE"; then
        echo "$line" >> "$ENV_FILE"
        echo "Added: $line"
    fi
done < "$SAMPLE_FILE"

echo "Updating .env has been completed!"
