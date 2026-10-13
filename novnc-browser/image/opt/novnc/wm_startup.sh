#!/bin/bash

set -e

echo "starting openbox"

openbox 2>/tmp/openbox_stderr.log &

# Wait for the window manager to announce itself on the root window
timeout=300
while [ $timeout -gt 0 ]; do
    if xprop -root _NET_SUPPORTING_WM_CHECK 2>/dev/null | grep -q "window id"; then
        break
    fi
    sleep 0.1
    ((timeout--))
done

if [ $timeout -eq 0 ]; then
    echo "openbox did not announce itself, processes and root property:" >&2
    pgrep -a openbox >&2 || echo "openbox not running" >&2
    xprop -root _NET_SUPPORTING_WM_CHECK >&2
    echo "openbox stderr output:" >&2
    cat /tmp/openbox_stderr.log >&2
    exit 1
fi

rm /tmp/openbox_stderr.log
