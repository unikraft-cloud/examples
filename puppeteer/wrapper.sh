#!/bin/sh

set -e

export HOME=/root
cd /src
exec "$@"
