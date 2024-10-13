#!/bin/bash

set -e

export JAVA_HOME=/opt/java/openjdk/
export SPARK_NO_DAEMONIZE=1
hostname spark-worker
exec "$@" spark://"$SPARK_MASTER_HOST":"$SPARK_MASTER_PORT"
