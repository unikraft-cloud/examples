#!/usr/bin/env bash

set -e

# Set defaults from official dockerfile
echo "Loading environment variables from embedded env file..."

# Check if environment file exists (will be created at build time)
if [[ -f /minecraft_env.txt ]]; then
    echo "Found environment file. Processing variables:"
    while IFS='=' read -r key value; do
        if [[ -n "$key" && -n "$value" ]]; then
            # Remove quotes from value if present
            value=$(echo "$value" | sed 's/^"//;s/"$//')
            echo "Setting $key=$value"
            export "$key"="$value"
        fi
    done < /minecraft_env.txt
else
    echo "WARNING: No environment file found. Setting basic defaults..."
    export EULA="TRUE"
    export TYPE="VANILLA"
    export VERSION="LATEST"
fi

echo ""
echo "Current environment after setup:"
env | sort

echo ""
echo "Environment setup complete. Continuing from the original entrypoint..."
exec "$@"
