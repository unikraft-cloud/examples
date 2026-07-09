# Unikraft Cloud Port Mapping

This guide presents how to expose an application running on Unikraft Cloud by mapping an external port to the internal port used by the application. In particular, it shows how to use the Port Mapping feature to expose a Python HTTP server listening on port `8080` through HTTPS on external port `443`.

Namely, the guide presents:

- deploying an instance with port mapping
- creating an image
- pushing an image
- creating an instance with an exposed port
- starting an instance
- listing instances
- listing images
- getting information about an instance
- querying the deployed application
- getting logs from an instance
- stopping an instance
- deleting an instance

The guide explains how to do the above both using the `kraft` CLI tool and directly using the underlying Unikraft Cloud platform API.

The target application used in this guide is a simple Python HTTP server.

# Contents

- `server.py`: the simple Python HTTP server app to be deployed on Unikraft Cloud
- `Dockerfile`: the Dockerfile to build the OCI image running the HTTP server app
- `Kraftfile`: the Unikraft Cloud specification file describing how to operate the image
- `ukc.config.template`: a template configuration file for Unikraft Cloud
- `api/`: scripts used to directly interact with the Unikraft Cloud platform API
- `README.md`: this file

# Prerequisites

1. Install the `kraft` CLI tool.
2. Install and configure Docker.
3. (Optional, but recommended) Configure BuildKit.
4. Create an Unikraft Cloud account.

# Set Up

Create a `ukc.config` file as a copy of the `ukc.config.template`. Replace the `TODO` entries in the `ukc.config` file with your corresponding Unikraft Cloud configuration values: user, token and metro.

```bash
cp ukc.config.template ukc.config
```

Load the configuration:

```bash
source ukc.config
```

# TLDR: Deploy and Operate an Instance

Below are the commands used to deploy and operate an instance with the `kraft` CLI.

```bash
source ukc.config

kraft cloud deploy \
    -M 256M \
    -p 443:8080/tls+http \
    --name port-mapping-demo .

kraft cloud image list
kraft cloud instance list
kraft cloud instance get port-mapping-demo
kraft cloud instance get port-mapping-demo -o table

fqdn=https://$(kraft cloud instance get port-mapping-demo -o json 2>/dev/null | jq -r '.data.instances[] | select(.name == "port-mapping-demo") | .service_group.domains[0].fqdn')

curl -k "$fqdn"

kraft cloud instance logs port-mapping-demo
kraft cloud instance stop port-mapping-demo
sleep 2
kraft cloud instance start port-mapping-demo
kraft cloud instance delete port-mapping-demo
kraft cloud instance list
```

# TLDR: Pack and Push an Image and Operate an Instance

Below are the commands used to pack and push an image and operate an instance with the `kraft` CLI.

```bash
source ukc.config

kraft pkg --plat kraftcloud --arch x86_64 --name index.unikraft.io/"$UKC_USER"/port-mapping:latest .
kraft pkg push index.unikraft.io/"$UKC_USER"/port-mapping:latest

kraft cloud image list

kraft cloud instance create \
    -M 256M \
    -p 443:8080/tls+http \
    --name port-mapping-demo \
    index.unikraft.io/"$UKC_USER"/port-mapping:latest

kraft cloud instance start port-mapping-demo
kraft cloud instance list
kraft cloud instance get port-mapping-demo
kraft cloud instance get port-mapping-demo -o table

fqdn=https://$(kraft cloud instance get port-mapping-demo -o json 2>/dev/null | jq -r '.data.instances[] | select(.name == "port-mapping-demo") | .service_group.domains[0].fqdn')

curl -k "$fqdn"

kraft cloud instance logs port-mapping-demo
kraft cloud instance stop port-mapping-demo
sleep 2
kraft cloud instance start port-mapping-demo
kraft cloud instance delete port-mapping-demo
kraft cloud instance list
```

# TLDR: Pack and Push an Image and Operate an Instance via the API

Below are the commands used to deploy and operate an instance via the Unikraft Cloud Platform API.

```bash
./api/pkg-image.sh
./api/push-image.sh
./api/create-instance.sh
./api/start-instance.sh
./api/get-instance-info.sh
./api/query.sh
./api/stop-instance.sh
./api/delete-instance.sh
```

# Detailed Operations with the Kraft CLI

## Source Configuration File

```bash
source ukc.config
```

This command loads the Unikraft Cloud configuration parameters: user, token and metro.

## All-in-One Package, Push, Create and Start Deploy

```bash
kraft cloud deploy \
    -M 256M \
    -p 443:8080/tls+http \
    --name port-mapping-demo .
```

This command packages the image locally, pushes it to the remote Unikraft Cloud registry, creates an instance and starts it.

The `-p 443:8080/tls+http` flag configures port mapping. It exposes port `443` externally and forwards the traffic to port `8080` inside the instance.

## Create Package Image

```bash
kraft pkg --plat kraftcloud --arch x86_64 --name index.unikraft.io/"$UKC_USER"/port-mapping:latest .
kraft pkg list --all
```

## Push Image

```bash
kraft pkg push index.unikraft.io/"$UKC_USER"/port-mapping:latest
```

## List Remote Images

```bash
kraft cloud image list
```

## Create Instance

```bash
kraft cloud instance create \
    -M 256M \
    -p 443:8080/tls+http \
    --name port-mapping-demo \
    index.unikraft.io/"$UKC_USER"/port-mapping:latest
```

This creates an instance and maps external port `443` to internal port `8080`.

## Start Instance

```bash
kraft cloud instance start port-mapping-demo
```

## List Instances

```bash
kraft cloud instance list
```

## Get Information about an Instance

```bash
kraft cloud instance get port-mapping-demo
kraft cloud instance get port-mapping-demo -o table
```

## Query Instance

```bash
fqdn=https://$(kraft cloud instance get port-mapping-demo -o json 2>/dev/null | jq -r '.data.instances[] | select(.name == "port-mapping-demo") | .service_group.domains[0].fqdn')
curl -k "$fqdn"
```

## Get Instance Logs

```bash
kraft cloud instance logs port-mapping-demo
```

## Stop Instance

```bash
kraft cloud instance stop port-mapping-demo
```

## Delete Instance

```bash
kraft cloud instance delete port-mapping-demo
```

# Detailed Operations with the Unikraft Cloud Platform API

Below are detailed commands to deploy and operate instances with the Unikraft Cloud Platform API. The commands are scripts from the `api/` directory. These scripts make HTTP requests using `curl` to the REST API exposed by the platform.

Note: image-related operations do not directly interact with the platform API. Therefore, for creating and pushing images, the scripts use the `kraft` CLI tool, similarly to the CLI workflow.

## Create Package Image

```bash
./api/pkg-image.sh
```

## Push Image

```bash
./api/push-image.sh
```

## Create Instance

```bash
./api/create-instance.sh
```

This script is the core of the example. It creates an instance through the Unikraft Cloud Platform API and explicitly configures the port mapping in the request payload.

The request payload includes:

```json
"service_group": {
    "services": [
        {
            "port": 443,
            "destination_port": 8080,
            "handlers": ["tls", "http"]
        }
    ]
}
```

This maps the external port `443` to the internal application port `8080`.

## Start Instance

```bash
./api/start-instance.sh
```

## Get Information about an Instance

```bash
./api/get-instance-info.sh
```

## Query Instance

```bash
./api/query.sh
```

## Stop Instance

```bash
./api/stop-instance.sh
```

## Delete Instance

```bash
./api/delete-instance.sh
```
