#!/bin/bash

# Folosire: ./create.sh <nume> <imagine> <policy> [memory_mb]
# Exemplu:  ./create.sh restart-never grobeert/restart-demo:latest never 256

NAME=$1
IMAGE=$2
POLICY=$3
MEMORY=${4:-256}

curl -s \
  -X POST \
  -H "Authorization: Bearer $UKC_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$NAME\",
    \"image\": \"$IMAGE\",
    \"memory_mb\": $MEMORY,
    \"restart_policy\": \"$POLICY\",
    \"autostart\": true
  }" \
  https://api.fra.unikraft.cloud/v1/instances \
  | jq .

