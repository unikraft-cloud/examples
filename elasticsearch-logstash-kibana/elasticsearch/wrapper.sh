#!/bin/bash

set -e

chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data

su elasticsearch -c "/usr/local/bin/docker-entrypoint.sh eswrapper"
