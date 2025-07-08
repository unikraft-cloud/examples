#!/usr/bin/env bash

set -e
docker inspect itzg/minecraft-server:latest | jq -r '.[0].Config.Env[]' | grep -v '^UID=' | grep -v '^GID=' > minecraft_env.txt
cat minecraft_env.txt
