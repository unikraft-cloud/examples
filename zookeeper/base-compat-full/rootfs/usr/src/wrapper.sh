#!/bin/bash

export PATH=/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/apache-zookeeper-3.7.2-bin/bin
export JAVA_HOME=/opt/java/openjdk
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export JAVA_VERSION=jdk-11.0.22+7
export ZOO_CONF_DIR=/conf
export ZOO_DATA_DIR=/data
export ZOO_DATA_LOG_DIR=/datalog
export ZOO_LOG_DIR=/logs
export ZOO_TICK_TIME=2000
export ZOO_INIT_LIMIT=5
export ZOO_SYNC_LIMIT=2
export ZOO_AUTOPURGE_PURGEINTERVAL=0
export ZOO_AUTOPURGE_SNAPRETAINCOUNT=3
export ZOO_MAX_CLIENT_CNXNS=60
export ZOO_STANDALONE_ENABLED=true
export ZOO_ADMINSERVER_ENABLED=true
export ZOOCFGDIR=/conf

exec "$@"
