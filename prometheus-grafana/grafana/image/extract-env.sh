#!/usr/bin/env bash

set -e
docker pull grafana/grafana:12.0.2
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' grafana/grafana:12.0.2 > env.txt
echo ""
echo "Environment variables extracted to env.txt:"
cat env.txt
