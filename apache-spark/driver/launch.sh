#!/bin/sh

kraft cloud instance create --scale-to-zero off --start -M 4096 --name apache-spark-driver --subdomain apache-spark-driver razvan.unikraft.io/apache-spark-driver
