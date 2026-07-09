#!/bin/sh

. ./ukc.config
. ./app.config

curl \
    --silent \
    -X PUT \
    -H "Authorization: Bearer ${UKC_TOKEN}" \
    -H "Content-Type: application/json" \
    "${UKC_METRO}/instances/stop" \
    -d "{
        'name': '${INSTANCE_NAME}'
    }" | jq
