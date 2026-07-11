#!/bin/bash

# Verify the autoscale configuration applied by the deploy tool
# Usage: ./unikraft/scale.sh

# Aici poți folosi numele sau UUID-ul serviciului tău
GROUP_NAME="wandering-snow-h5bi22ct"

echo "[+] Verifying Unikraft deploy autoscale status for $GROUP_NAME..."
unikraft service get "$GROUP_NAME"