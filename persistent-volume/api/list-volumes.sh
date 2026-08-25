#!/bin/bash
# list-volumes.sh

curl -X GET "https://api.${UKC_METRO}.unikraft.cloud/v1/volumes" \
  -H "Authorization: Bearer $UKC_TOKEN" \
  -H "Content-Type: application/json"

