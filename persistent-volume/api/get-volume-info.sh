#!/bin/bash
# get-volume-info.sh

curl -X GET "https://api.${UKC_METRO}.unikraft.cloud/v1/volumes" \
  -H "Authorization: Bearer $UKC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"name": "storage-vol-01"}]'
