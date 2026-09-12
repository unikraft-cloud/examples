#!/bin/sh

. ./ukc.config
. ./app.config

curl \
    --silent \
    -X GET \
    -H "Authorization: Bearer ${UKC_TOKEN}" \
    -H "Content-Type: application/json" \
    "${UKC_API}/instances" \
    -d "
[
    {
        'name': '${INSTANCE_NAME}'
    }
]
" | jq
