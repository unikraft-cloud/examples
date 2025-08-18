#!/usr/bin/env bash

set -e

# Set defaults from official dockerfile
echo "Loading environment variables from embedded env file..."

# Check if environment file exists (will be created at build time)
if [[ -f /env.txt ]]; then
    echo "Found environment file. Processing variables:"
    while IFS='=' read -r key value; do
        if [[ -n "$key" && -n "$value" ]]; then
            # Remove quotes from value if present
            value=$(echo "$value" | sed 's/^"//;s/"$//')
            echo "Setting $key=$value"
            export "$key"="$value"
        fi
    done < /env.txt
else
    echo "WARNING: No environment file found. Setting basic defaults..."
    export TYPE="VANILLA"
    export VERSION="LATEST"
fi

# Add extra configuration
export EULA="TRUE"
export ENABLE_COMMAND_BLOCK="true"
export MEMORY="2G"
export SNOOPER_ENABLED="false"
export ONLINE_MODE="false"
## Uncomment below if you want to push a custom resource pack
# export RESOURCE_PACK=""
# export RESOURCE_PACK_SHA1=""
# export RESOURCE_PACK_ENFORCE="true"
## Uncomment below if you want to use a custom world
# export WORLD="/worlds/world"
## Uncomment below if you want to specify a specific version
# export VERSION="1.19.2"

echo ""
echo "Current environment after setup:"
env | sort

echo ""
echo "Environment setup complete. Continuing from the original entrypoint..."
exec "$@"
