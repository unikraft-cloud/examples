#!/bin/bash

# Folosire: ./create.sh <nume> <imagine> <policy> [memory_mb]
# Exemplu:  ./create.sh restart-never grobeert/restart-demo:latest never 256

NAME=$1
IMAGE=$2
POLICY=$3
METRO=${UKC_METRO:-fra}

payload=$(jq -n \
   --arg name "$NAME" \
   --arg image "$IMAGE" \
   --arg policy "$POLICY" \
   --argjson memory_mb "$MEMORY" \
   '{name: $name, image: $image, memory_mb: $memory_mb, restart_policy: $policy, autostart: true}'
 )
 curl -s \
   -X POST \
   -H "Authorization: Bearer $UKC_TOKEN" \
   -H "Content-Type: application/json" \
   -d "$payload" \
   "https://api.${METRO}.unikraft.cloud/v1/instances" \
   | jq .