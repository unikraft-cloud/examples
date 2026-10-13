#!/bin/bash

set -e

export DISPLAY=:${DISPLAY_NUM}
./xvfb_startup.sh
./wm_startup.sh
./panel_startup.sh
./x11vnc_startup.sh
