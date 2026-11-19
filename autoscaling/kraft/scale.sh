#!/bin/bash

# Configure the autoscaling policy for a service group.
# Usage: ./scale.sh <service-group> <template-instance>
# Example: ./scale.sh my-scaling-group my-first-instance

GROUP=${1:-my-scaling-group}
TEMPLATE=${2:-my-first-instance}

echo "[+] Initializing autoscale configuration for service group $GROUP using template $TEMPLATE..."
# The template was already successfully created, so we just ensure the autoscaler is initialized
kraft cloud scale init $GROUP --min-size 0 --max-size 1 --template $TEMPLATE || true

echo "[+] Configuring CPU autoscaling policy..."
kraft cloud scale add $GROUP \
  --name my-cpu-policy \
  --metric cpu \
  --adjustment percent \
  --step 600:800/50 \
  --step 800:/100 || true