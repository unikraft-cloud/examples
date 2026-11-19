#!/bin/bash
set -e

IMAGE_NAME="calinachoo/my-autoscaling-app:latest"
METRO="fra"

echo "[+] Building the image via Unikraft CLI..."
unikraft build ./app --output "$IMAGE_NAME"

echo "[+] Deploying autoscaling infrastructure via Unikraft CLI..."

# Soluția: ne mutăm temporar într-un folder neutru pentru a forța CLI-ul
# să ignore vechiul kraft.yaml/Kraftfile care corupe cererea către API
cd /tmp

unikraft run \
  --scale-to-zero policy=on \
  --metro "$METRO" \
  -p 443:8080/tls+http \
  -m 512M \
  --image "$IMAGE_NAME"

echo -e "\n[+] Unikraft deploy request completed successfully."