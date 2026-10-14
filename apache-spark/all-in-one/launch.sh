#!/bin/sh

kraft cloud inst create --scale-to-zero off --start -M 4096 -p 443:8080/http+tls -p 444:8081/tls -p 7077:7077/tls --name apache-spark --subdomain apache-spark razvan.unikraft.io/apache-spark
