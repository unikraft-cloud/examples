#!/bin/bash
# attach-volume-deploy.sh

curl -X POST "https://api.${UKC_METRO}.unikraft.cloud/v1/instances" \
  -H "Authorization: Bearer $UKC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "storage-demo",
    "image": "dan-andrei-simionescu/storage-app:latest",
    "memory_mb": 256,
    "volumes": [
      {
        "name": "storage-vol-01",
        "at": "/data"
      }
    ],
    "autostart": true
  }'

