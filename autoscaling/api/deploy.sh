#!/bin/bash

# Deploy infrastructure using the raw Unikraft Cloud REST API
# Usage: ./api/deploy.sh

TOKEN="${UKC_TOKEN}"
METRO="${UKC_METRO:-fra}"
API_URL="https://api.${METRO}.unikraft.cloud/v1"
GROUP_NAME="my-scaling-group"

if [ -z "$TOKEN" ]; then
    echo "[-] Error: UKC_TOKEN is not set. Please export it before running."
    exit 1
fi

echo "[+] Creating service group '$GROUP_NAME' via Unikraft Cloud API..."
curl -s -X POST "${API_URL}/services" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${GROUP_NAME}\",
    \"services\": [
      {
        \"port\": 443,
        \"destination_port\": 8080,
        \"handlers\": [\"http\", \"tls\"]
      }
    ]
  }"

echo -e "\n[+] Service group deployment request sent successfully."