#!/bin/bash

echo "starting lxpanel on display :$DISPLAY_NUM ..."

lxpanel --profile default 2>/tmp/lxpanel_stderr.log &

# Wait for the panel window to appear
timeout=300
while [ $timeout -gt 0 ]; do
    if xdotool search --classname "lxpanel" >/dev/null 2>&1; then
        break
    fi
    sleep 0.1
    ((timeout--))
done

if [ $timeout -eq 0 ]; then
    echo "lxpanel stderr output:" >&2
    cat /tmp/lxpanel_stderr.log >&2
    exit 1
fi

rm /tmp/lxpanel_stderr.log
