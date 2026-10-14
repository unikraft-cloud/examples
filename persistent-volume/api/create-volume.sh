#!/usr/bin/env bash
# create-volume.sh

curl -X POST "https://api.${UKC_METRO}.unikraft.cloud/v1/volumes" \
  -H "Authorization: Bearer $UKC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "storage-vol-01",
    "size_mb": 9
  }'
