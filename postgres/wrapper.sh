#!/usr/bin/env bash
set -e
# Set defaults from offical dockerfile
if [ -z "$LANG" ]; then
    export LANG=en_US.utf8
fi
export PG_MAJOR=16
export PG_VERSION=16.2

if [ -z "$PGDATA" ]; then
    export PGDATA=/var/lib/postgresql/data
fi

exec "$@"
