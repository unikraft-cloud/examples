#!/bin/sh

socat tcp-listen:7077,bind=127.0.0.1,fork,reuseaddr openssl:apache-spark.fra0.kraft.host:7077 &
