#!/bin/sh

cd /src
export PATH=/usr/bin:/usr/local/bin
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export LANGUAGE=C.UTF-8
export MIX_HOME=/root/.mix
exec $@
