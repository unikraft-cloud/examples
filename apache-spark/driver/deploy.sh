#!/bin/sh

kraft cloud deploy --scale-to-zero off -M 4096 -p 443--scale-to-zero off :8080/http+tls -p 7077:7077/tls --name apache-spark-driver --subdomain apache-spark-driver .
