#!/bin/bash
 
# Folosire: ./list.sh
 
METRO=${UKC_METRO:-fra}

curl -s \
  -H "Authorization: Bearer $UKC_TOKEN" \
  "https://api.${METRO}.unikraft.cloud/v1/instances" \
  | jq .
