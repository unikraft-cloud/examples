#!/bin/bash

set -e

export JAVA_HOME=/opt/java/openjdk/
hostname apache-spark
export SPARK_NO_DAEMONIZE=1
/opt/spark/sbin/start-master.sh &
/opt/spark/sbin/start-worker.sh spark://localhost:7077
