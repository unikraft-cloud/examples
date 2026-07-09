#!/bin/bash
 
# Folosire: ./list.sh
 
curl -s \
  -H "Authorization: Bearer $UKC_TOKEN" \
  https://api.fra.unikraft.cloud/v1/instances \
  | jq .
