#!/bin/sh

. ./ukc.config
. ./app.config

curl \
    --silent \
    -X PUT \
    -H "Authorization: Bearer ${UKC_TOKEN}" \
    -H "Content-Type: application/json" \
    "${UKC_METRO}/instances/start" \
    -d "{
        'name': '${INSTANCE_NAME}'
    }" | jq
