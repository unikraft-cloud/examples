#!/usr/bin/env sh
set -e

# BACKEND_HOST defaults to backend.internal if not set.
BACKEND_HOST="${BACKEND_HOST:-backend.internal}"
export BACKEND_HOST

# Substitute environment variables into the NGINX template.
envsubst '${BACKEND_HOST}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec nginx
