#!/bin/sh

. ./ukc.config
. ./app.config

MEMORY_MB=${1:-${MEMORY_MB}}
VCPUS=${2:-${VCPUS}}

curl \
    --silent \
    -X POST \
    -H "Authorization: Bearer ${UKC_TOKEN}" \
    -H "Content-Type: application/json" \
    "${UKC_API}/instances" \
    -d "{
        'name': '${INSTANCE_NAME}',
        'image': '${UKC_USER}/${IMAGE_NAME}:latest',
        'service_group': {
            'services': [
                {
                    'port': 443,
                    'destination_port': 8080,
                    'handlers': [
                        'tls',
                        'http'
                    ]
                }
            ],
            'domains': [
                {
                    'name': '${INSTANCE_NAME}'
                }
            ]
        },
        'memory_mb': ${MEMORY_MB},
        'vcpus': ${VCPUS}
    }" | jq
