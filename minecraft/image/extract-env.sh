#!/usr/bin/env bash

set -e
docker pull itzg/minecraft-server:latest
docker inspect itzg/minecraft-server:latest | jq -r '.[0].Config.Env[]' | grep -v '^UID=' | grep -v '^GID=' > env.txt
cat env.txt
