#!/bin/bash

# Configure autoscale policy using the raw Unikraft Cloud REST API
# Usage: ./api/scale.sh

TOKEN="${UKC_TOKEN}"
METRO="${UKC_METRO:-fra}"
API_URL="https://api.${METRO}.unikraft.cloud/v1"
GROUP_NAME="my-scaling-group"
TEMPLATE_NAME="my-first-instance"

if [ -z "$TOKEN" ]; then
    echo "[-] Error: UKC_TOKEN is not set. Please export it before running."
    exit 1
fi

echo "[+] Configuring autoscale policy for '$GROUP_NAME' via API..."
# Changed the identifier key to "name" to match the root properties of the cloud resource
curl -s -X POST "${API_URL}/services/autoscale" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${GROUP_NAME}\",
    \"min_size\": 0,
    \"max_size\": 1,
    \"create_args\": {
      \"template\": {
        \"name\": \"${TEMPLATE_NAME}\"
      }
    },
    \"policies\": [
      {
        \"name\": \"my-cpu-policy\",
        \"type\": \"step\",
        \"metric\": \"cpu\",
        \"adjustment_type\": \"percent\",
        \"steps\": [
          { \"lower_bound\": 600, \"upper_bound\": 800, \"adjustment\": 50 },
          { \"lower_bound\": 800, \"adjustment\": 100 }
        ]
      }
    ]
  }"

echo -e "\n[+] Autoscale policy configuration request sent successfully."