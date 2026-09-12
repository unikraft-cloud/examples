#!/bin/sh

. ./ukc.config
. ./app.config

curl \
    --silent \
    -X GET \
    -H "Authorization: Bearer ${UKC_TOKEN}" \
    -H "Content-Type: application/json" \
    "${UKC_API}/instances/log" \
    -d "
[
    {
        'name': '${INSTANCE_NAME}',
        'offset': 0,
        'limit': 5000
    }
]
" > out 2> err

if test $? -ne 0; then
    cat err 1>&2
else
    status=$(cat out | jq -r .status)
    if test "$status" = "error"; then
        cat out | jq
    else
        cat out | jq -r .data.instances[0].output | base64 -d
    fi
fi

rm -f out err
