#!/bin/bash

# Folosire: ./delete.sh <uuid>
# Exemplu:  ./delete.sh 1fa6c541-10e5-4ca8-8828-7597c6facc58

UUID=$1

curl -s \
  -X DELETE \
  -H "Authorization: Bearer $UKC_TOKEN" \
  https://api.fra.unikraft.cloud/v1/instances/$UUID \
  | jq .