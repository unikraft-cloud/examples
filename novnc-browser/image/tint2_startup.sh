#!/bin/bash

echo "starting tint2 on display :$DISPLAY_NUM ..."

# Verify the X display is still reachable. If Xvfb came up, passed its
# readiness check, and then exited (e.g. a rootfs artifact that is subtly
# wrong on emulated builds), tint2 would otherwise just print "could not
# open display!" and we would burn the full 30s timeout below with no clue.
if ! xdpyinfo >/dev/null 2>&1; then
    echo "ERROR: display :$DISPLAY_NUM is not reachable - Xvfb appears to have exited after startup" >&2
    if [ -f /tmp/xvfb_stderr.log ]; then
        echo "Xvfb stderr output:" >&2
        cat /tmp/xvfb_stderr.log >&2
    fi
    exit 1
fi

# Start tint2 and capture its stderr
tint2 -c $HOME/.config/tint2/tint2rc 2>/tmp/tint2_stderr.log &

# Wait for tint2 window properties to appear
timeout=30
while [ $timeout -gt 0 ]; do
    if xdotool search --class "tint2" >/dev/null 2>&1; then
        break
    fi
    sleep 1
    ((timeout--))
done

if [ $timeout -eq 0 ]; then
    echo "tint2 stderr output:" >&2
    cat /tmp/tint2_stderr.log >&2
    exit 1
fi

# Remove the temporary stderr log file
rm /tmp/tint2_stderr.log
