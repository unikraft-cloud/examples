#!/bin/bash

set -e

export JAVA_HOME=/opt/java/openjdk/
hostname apache-spark-driver
export MASTER=spark://apache-spark.kraft.host:7077
/opt/spark/bin/run-example --conf spark.scheduler.minRegisteredResourcesRatio=0 SparkPi
