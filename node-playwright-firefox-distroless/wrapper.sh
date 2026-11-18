#!/bin/sh

set -e

chown root:root /root

export HOME=/root

cd /app
exec "$@"
