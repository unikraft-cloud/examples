#!/bin/bash

# Deploy an instance and assign it to a service group.
# Usage: ./deploy.sh <instance-name> <service-group>
# Example: ./deploy.sh my-first-instance my-scaling-group

NAME=${1:-my-first-instance}
GROUP=${2:-my-scaling-group}

echo "[+] Creating service group $GROUP (if it doesn't exist)..."
# Create the service group. We use '|| true' so the script doesn't fail if the group already exists.
kraft cloud service create -n $GROUP 443:8080/http+tls || true

echo "[+] Deploying instance $NAME to service group $GROUP..."
# We append ./app at the end to explicitly tell KraftKit where the Kraftfile and Dockerfile are located.
kraft cloud deploy -M 512M -g $GROUP --name $NAME ./app