#!/bin/sh

. ./ukc.config
. ./app.config

API_URL="https://api.${UKC_METRO}.unikraft.cloud/v1"

curl --silent -X POST \
  -H "Authorization: Bearer ${UKC_TOKEN}" \
  -H "Content-Type: application/json" \
  "${API_URL}/instances" \
  -d "{
    \"name\": \"${INSTANCE_NAME}\",
    \"image\": \"${UKC_USER}/${IMAGE_NAME}:latest\",
    \"memory_mb\": 256,
    \"service_group\": {
      \"services\": [{
        \"port\": 443,
        \"destination_port\": 8080,
        \"handlers\": [\"tls\", \"http\"]
      }],
      \"domains\": [{
        \"name\": \"${INSTANCE_NAME}\"
      }]
    }
  }" > out 2> err


if test $? -ne 0; then
    cat err 1>&2
else
    cat out | jq
fi

#echo "Response:"
#cat out

#echo
#echo "Errors:"
#cat err

rm -f out err
