#!/usr/bin/env bash

set -e

# Set defaults from official dockerfile
echo "Loading environment variables from embedded env file..."

# Check if environment file exists (will be created at build time)
if [[ -f ./env.txt ]]; then
    echo "Found environment file. Processing variables:"
    while IFS='=' read -r key value; do
        if [[ -n "$key" && -n "$value" ]]; then
            # Remove quotes from value if present
            value=$(echo "$value" | sed 's/^"//;s/"$//')
            echo "Setting $key=$value"
            export "$key"="$value"
        fi
    done < ./env.txt
else
    echo "No environment file found. Please run extract-env.sh to generate it."
    exit 1
fi

echo ""
echo "Current environment after setup:"
env | sort

echo ""
echo "Environment setup complete. Continuing from the original entrypoint..."
exec "$@"
