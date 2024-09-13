#!/bin/sh

set -e

export HOME=/root
cd /app
. .venv/bin/activate
exec "$@"
