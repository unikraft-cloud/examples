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
        'name': '${INSTANCE_NAME}',
      }" > out 2> err

if test $? -ne 0; then
    cat err 1>&2
else
    cat out | jq
fi

rm -f out err
