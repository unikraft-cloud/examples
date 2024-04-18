#!/bin/sh

set -e

if [ -z "$BINDIR" ]; then
    export BINDIR=/usr/lib/erlang/erts-13.1.5/bin
fi

/bin/rm /dev/null
/bin/mknod -m 0666 /dev/null c 1 3

cd /usr/src/
exec "$@"
