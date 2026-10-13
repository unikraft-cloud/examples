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

# Apply the configuration
eval "$(python3 ./config.py "${NOVNC_CONFIG:-/etc/novnc/config.json}")"

# Start dependencies
./start_all.sh

for cmd in "${AUTOSTART[@]}"; do
    echo "autostart: $cmd"
    setsid sh -c "$cmd" >/dev/null 2>&1 &
done

auth=()
if [ -n "${NOVNC_AUTH_FILE:-}" ]; then
    auth=(--web-auth --auth-plugin novnc_auth.FileBasicAuth
          --auth-source "$NOVNC_AUTH_FILE")
else
    echo "WARNING: noVNC has no authentication, set 'password' in the configuration or NOVNC_PASSWORD" >&2
fi

# Start the noVNC web server and the WebSocket proxy to x11vnc
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
exec /opt/noVNC/utils/websockify/run \
    --web /opt/noVNC \
    "${auth[@]}" \
    "${NOVNC_PORT:-6080}" 127.0.0.1:5900
