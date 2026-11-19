#!/bin/sh

kraft cloud deploy --scale-to-zero off -M 4096 -p 443:8080/http+tls -p 7077:7077/tls --name apache-spark --subdomain apache-spark .
