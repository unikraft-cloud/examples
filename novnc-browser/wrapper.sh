#!/usr/bin/env bash

set -e

export HOME="${HOME:-/root}"
export DEBIAN_FRONTEND=noninteractive
export DEBIAN_PRIORITY=high
export DISPLAY_NUM=1
export DISPLAY=":${DISPLAY_NUM}"
export HEIGHT=768
export WIDTH=1024
export XDG_MENU_PREFIX=lxde-

cd "$(dirname "$0")"

# Apply the configuration. Only config.py sets the auth file.
unset NOVNC_AUTH_FILE
config="$(python3 ./config.py "${NOVNC_CONFIG:-/etc/novnc/config.json}")"
eval "$config"

# Start dependencies
./start_all.sh

for cmd in "${AUTOSTART[@]}"; do
    echo "autostart: $cmd"
    setsid sh -c "$cmd" >/dev/null 2>&1 &
done

if [ -z "${NOVNC_AUTH_FILE:-}" ]; then
    echo "WARNING: noVNC has no authentication, set 'password' in the configuration or NOVNC_PASSWORD" >&2
fi

# Start the noVNC web server and the WebSocket proxy to x11vnc
export PYTHONPATH="/opt/noVNC/utils/websockify${PYTHONPATH:+:$PYTHONPATH}"
exec python3 ./novnc_server.py "${NOVNC_PORT:-6080}" "${NOVNC_AUTH_FILE:-}"
