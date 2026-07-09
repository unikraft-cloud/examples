# Unikraft Cloud Autoscaling Demo

> Status: Work in progress.

## Overview

This example demonstrates how to configure autoscaling for applications running on Unikraft Cloud.

The guide covers:
- deploying an application
- initializing autoscaling
- configuring CPU-based autoscaling
- configuring network-based autoscaling
- generating load
- monitoring created instances
- cleaning up resources

The guide explains how to configure autoscaling using both the `kraft` CLI tool and the underlying Unikraft Cloud Platform API.

The target application used in this guide is a simple Python HTTP server.

## Contents
- `server.py` - simple Python HTTP server used to demonstrate autoscaling
- `Dockerfile` - builds the OCI image containing the application
- `Kraftfile` - Unikraft Cloud deployment specification
- `ukc.config.template` – template configuration file
- `generate_load.py` – generates HTTP requests to trigger autoscaling
- `api/` – scripts interacting directly with the Unikraft Cloud Platform API
- `README.md` – this guide

## Prerequisites
1. Install `kraft` CLI tool
2. Install and configure Docker.
3. (Optional, but recommended) Configure BuildKit.
4. Create an Unikraft Cloud account.

## Set up

### Clone the repository

```bash
git clone https://github.com/<your-username>/examples.git
cd examples/autoscaling
```

### Configure Unikraft Cloud

Create a configuration file from the provided template:

```bash
cp ukc.config.template ukc.config
```

Edit `ukc.config` and set the following values:

- `UKC_USER`
- `UKC_TOKEN`
- `UKC_METRO`

Load the configuration:

```bash
source ukc.config
```

### Verify the installation

Check that the `kraft` CLI is installed:

```bash
kraft version
```

Optionally, verify Docker:

```bash
docker --version
```

## TLDR: Deploy and Configure Autoscaling

Below are the commands used to deploy and configure autoscaling (with the `kraft` CLI). You can copy-paste them:

```bash
source ukc.config

kraft cloud deploy \
    -p 443:8080/tls+http \
    --name autoscaling-demo .

kraft cloud scale init autoscaling-demo

kraft cloud scale add autoscaling-demo \
    --metric cpu \
    --adjustment percent \
    --step 600:800/50 \
    --step 800:/100 \
    --min-size 1 \
    --max-size 5

python3 generate_load.py

kraft cloud instance list

curl https://<service-domain>
```

## TLDR: Configure Autoscaling via the API

Below are the commands used to deploy and configure autoscaling via the Unikraft Cloud Platform API. You can copy-paste them:

```bash
./api/pkg-image.sh
./api/push-image.sh
./api/create-instance.sh
./api/start-instance.sh
./api/init-autoscaling.sh
./api/add-autoscaling-policy.sh
./api/list-instances.sh
./api/generate-load.sh
```
### Clean Up

```bash
./api/stop-instance.sh
./api/delete-instance.sh
```
## Detailed Operations with the Kraft CLI

### Source Configuration File

```bash
source ukc.config
```

Loads the Unikraft Cloud configuration, including the user, token and metro.

### Deploy Application

```bash
kraft cloud deploy \
    -p 443:8080/tls+http \
    --name autoscaling-demo .
```

Packages the application, pushes it to Unikraft Cloud, creates an instance and starts it.

### Initialize Autoscaling

```bash
kraft cloud scale init autoscaling-demo
```

Creates the autoscaling configuration for the deployed service.

### Configure Autoscaling

```bash
kraft cloud scale add autoscaling-demo \
    --metric cpu \
    --adjustment percent \
    --step 600:800/50 \
    --step 800:/100 \
    --min-size 1 \
    --max-size 5
```

This command creates an autoscaling policy for the deployed service. The platform continuously monitors the selected metric and automatically adjusts the number of running instances according to the configured thresholds.

### Generate Traffic

```bash
python3 generate_load.py
```

Sends HTTP requests to the application in order to trigger autoscaling.

### Monitor Instances

```bash
kraft cloud instance list
```

Lists the running instances. When autoscaling is triggered, new instances should appear.

### Query the Application

```bash
curl https://<service-domain>
```

Checks that the application is still responding.

### Clean Up

```bash
kraft cloud instance stop autoscaling-demo
kraft cloud instance delete autoscaling-demo
```

Stops and removes the deployed application.

## Detailed Operations with the Unikraft Cloud Platform API

The following scripts provide the API equivalent of the Kraft CLI workflow presented above.

### Package the Application

```bash
./api/pkg-image.sh
```

Packages the application into an OCI image.

### Push the Image

```bash
./api/push-image.sh
```

Pushes the generated image to the Unikraft Cloud registry.

### Create an Instance

```bash
./api/create-instance.sh
```

Creates a new instance using the uploaded image.

### Start the Instance

```bash
./api/start-instance.sh
```

Starts the previously created instance.

### Initialize Autoscaling

```bash
./api/init-autoscaling.sh
```

Initializes the autoscaling configuration for the deployed service.

### Add an Autoscaling Policy

```bash
./api/add-autoscaling-policy.sh
```

Creates an autoscaling policy by sending the appropriate requests to the Unikraft Cloud Platform API.

### List Running Instances

```bash
./api/list-instances.sh
```

Displays all running instances associated with the service.

### Generate Load

```bash
./api/generate-load.sh
```

Generates HTTP traffic to trigger the configured autoscaling policy.

### Stop the Instance

```bash
./api/stop-instance.sh
```

Stops the running instance.

### Delete the Instance

```bash
./api/delete-instance.sh
```

Deletes the instance and removes the deployed application.

