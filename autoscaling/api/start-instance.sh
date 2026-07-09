#!/bin/sh

. ./ukc.config
. ./app.config

API_URL="https://api.${UKC_METRO}.unikraft.cloud/v1"

#INSTANCE_UUID=$(curl --silent \
#  -H "Authorization: Bearer ${UKC_TOKEN}" \
#  "${API_URL}/instances" | jq -r ".data.instances[] | select(.name==\"${INSTANCE_NAME}\") | .uuid")
INSTANCE_UUID="f72f2836-4007-4ea9-865b-8a26677fdc2d"
echo "INSTANCE_NAME=$INSTANCE_NAME"
echo "API_URL=$API_URL"
curl \
    --silent \
    -X PUT \
    -H "Authorization: Bearer ${UKC_TOKEN}" \
    -H "Content-Type: application/json" \
    "${API_URiL}/instances/start" \
    -d "{
        \"name\": \"${INSTANCE_UUID}\",
      }" > out 2> err

if test $? -ne 0; then
    cat err 1>&2
else
    cat out | jq
fi

rm -f out err
