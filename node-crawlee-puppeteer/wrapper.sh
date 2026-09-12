#!/bin/sh

set -e

export HOME=/root
. /root/.bashrc
cd /app
exec "$@"
