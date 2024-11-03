#!/bin/sh

curl -X POST https://spark.fra0.kraft.host/v1/submissions/create \
--header "Content-Type:application/json;charset=UTF-8" \
--data '{
  "appResource": "",
  "sparkProperties": {
    "spark.master": "spark://master:7077",
    "spark.app.name": "Spark Pi",
    "spark.driver.memory": "1g",
    "spark.driver.cores": "1",
    "spark.jars": ""
  },
  "clientSparkVersion": "",
  "mainClass": "org.apache.spark.deploy.SparkSubmit",
  "environmentVariables": { },
  "action": "CreateSubmissionRequest",
  "appArgs": [ "/opt/spark/examples/src/main/python/pi.py", "10" ]
}'
