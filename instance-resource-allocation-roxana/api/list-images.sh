#!/bin/sh

. ./ukc.config

curl \
    --silent \
    -X GET \
    -H "Authorization: Bearer ${UKC_TOKEN}" \
    -H 'Content-Type: application/json' \
    "${UKC_METRO}/images/list" | jq
