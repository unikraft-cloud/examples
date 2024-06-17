#!/bin/sh

set -e

export HOME=/root
cd /app
exec "$@"
