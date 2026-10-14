#!/bin/bash

set -e

export JAVA_HOME=/opt/java/openjdk/
export SPARK_NO_DAEMONIZE=1
hostname apache-spark-master
#ln -sfn /proc/self/fd /dev/fd
exec "$@"
