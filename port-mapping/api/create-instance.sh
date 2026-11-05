#!/bin/sh

. ./ukc.config
. ./app.config

curl --silent \
	-X POST \
	-H "Authorization: Bearer ${UKC_TOKEN}" \
	-H "Content-Type: application/json" \
	"${UKC_API}/instances" \
	-d "{
		\"name\": \"${INSTANCE_NAME}\",
		\"image\": \"${UKC_USER}/${IMAGE_NAME}:latest\",
		\"memory_mb\": ${MEMORY_MB},
		\"vcpus\": ${VCPUS},
		\"autostart\": true,
		\"service_group\": {
			\"services\": [
				{
					\"port\": ${SOURCE_PORT},
					\"destination_port\": ${DESTINATION_PORT},
					\"handlers\": [\"tls\", \"http\"]
				}
			],
			\"domains\": [
				{
					\"name\": \"${INSTANCE_NAME}\"
				}
			]
		}
	}" | jq
