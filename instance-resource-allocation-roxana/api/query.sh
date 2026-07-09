#!/bin/sh

. ./ukc.config
. ./app.config

fqdn=https://$(./api/get-instance-info.sh | jq -r '.data.instances[] | select(.name == "'"${INSTANCE_NAME}"'") | .service_group.domains[0].fqdn')

curl -k "$fqdn"

