#!/bin/sh

set -e

export HOME=/root
export PATH=/usr/bin:/bin
cd /app
exec "$@"
