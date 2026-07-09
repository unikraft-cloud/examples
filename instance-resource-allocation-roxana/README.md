# Unikraft Cloud Instance Resource Allocation

This guide presents how to configure memory and virtual CPU allocation for instances running on Unikraft Cloud. In particular, it shows how to use the Instance Resource Allocation feature to explicitly assign memory and vCPUs to an instance at deployment or creation time.

Namely, the guide presents:

- deploying an instance with custom memory and vCPU values
- creating an image
- pushing an image
- creating an instance with explicit resource allocation
- starting an instance
- listing instances
- listing images
- getting information about an instance
- querying the deployed application
- getting logs from an instance
- stopping an instance
- deleting an instance

The guide explains how to do the above both using the kraft CLI tool and directly using the underlying Unikraft Cloud platform API.
The target application used in this guide is a simple Python HTTP server.

#Contents

- `server.py`: the simple Python HTTP server app to be deployed on Unikraft Cloud
- `Dockerfile`: the Dockerfile to build the OCI image running the HTTP server app
- `Kraftfile`: the Unikraft Cloud specification file describing how to operate the image
- `ukc.config.template`: a template configuration file for Unikraft Cloud
- `test_resources.py`: a simple test script for the deployed instance
- `api/`: scripts used to directly interact with the Unikraft Cloud platform API
- `README.md`: this file

#Prerequisites
1. Install the `kraft` CLI tool [kraft](https://unikraft.org/docs/cli/install).
2. Install and configure [Docker](https://github.com/unikraft-cloud/examples/tree/main/basic-ops).
3. (Optional, but recommended) Configure BuildKit [build](https://unikraft.com/docs/platform/troubleshooting#how-can-you-cache-the-apps-filesystem-for-faster-builds).

#Set Up

Create a `ukc.config` file as a copy of the `ukc.config.template`. Replace the `TODO` entries in the `ukc.config` file with your corresponding Unikraft Cloud configuration values: user, token and metro.

#TLDR: Deploy and Operate an Instance

Below are the commands used to deploy and operate an instance with the `kraft` CLI.

```
source ukc.config
kraft cloud deploy -M 256M -V 1 -p 443:8080/tls+http --name resource-server .
kraft cloud image list
kraft cloud instance list
kraft cloud instance get resource-server
kraft cloud instance get resource-server -o table
fqdn=https://$(kraft cloud instance get resource-server -o json 2>/dev/null | jq -r '.data.instances[] | select(.name == "resource-server") | .service_group.domains[0].fqdn')
curl "$fqdn"
python3 test_resources.py "$fqdn"
kraft cloud instance logs resource-server
kraft cloud instance stop resource-server
sleep 2
kraft cloud instance start resource-server
kraft cloud instance delete resource-server
kraft cloud instance list
```
 
# TLDR: Pack and Push an Image and Operate an Instance

Below are the commands used to pack and push an image and operate an instance with the `kraft` CLI.

```
source ukc.config
kraft pkg --plat kraftcloud --arch x86_64 --name index.unikraft.io/"$UKC_USER"/resource-server:latest .
kraft pkg push index.unikraft.io/"$UKC_USER"/resource-server:latest
kraft cloud image list
kraft cloud instance create -M 256M -V 1 -p 443:8080/tls+http --name resource-server index.unikraft.io/"$UKC_USER"/resource-server:latest
kraft cloud instance start resource-server
kraft cloud instance list
kraft cloud instance get resource-server
kraft cloud instance get resource-server -o table
fqdn=https://$(kraft cloud instance get resource-server -o json 2>/dev/null | jq -r '.data.instances[] | select(.name == "resource-server") | .service_group.domains[0].fqdn')
curl "$fqdn"
python3 test_resources.py "$fqdn"
kraft cloud instance logs resource-server
kraft cloud instance stop resource-server
sleep 2
kraft cloud instance start resource-server
kraft cloud instance delete resource-server
kraft cloud instance list
```

# TLDR: Pack and Push an Image and Operate an Instance via the API

Below are the commands used to deploy and operate an instance via the Unikraft Cloud Platform API.

```
./api/pkg-image.sh
./api/push-image.sh
./api/list-images.sh
./api/create-instance.sh 256 1
./api/start-instance.sh
./api/list-instances.sh
./api/get-instance-info.sh
./api/query.sh
./api/get-instance-logs.sh
./api/stop-instance.sh
./api/delete-instance.sh
./api/list-instances.sh
```
The `create-instance.sh` script accepts two optional arguments: the amount of memory in MiB and the number of vCPUs.

```
./api/create-instance.sh 512 2
```

# Detailed Operations with the Kraft CLI

## Source Configuration File

```
source ukc.config
```
This command loads the Unikraft Cloud configuration parameters (`user`, `token`, `metro`).

## All-in-One Package, Push, Create and Start (Deploy)

```
kraft cloud deploy -M 256M -V 1 -p 443:8080/tls+http --name resource-server .
```
This command packages the image locally, pushes it to the remote Unikraft Cloud registry, then creates and starts an instance from the image.
The `-M 256M` flag assigns 256 MiB of memory, while `-V 1` assigns 1 virtual CPU.

```
kraft cloud deploy -M 512M -V 2 -p 443:8080/tls+http --name resource-server .
```

## Create (Package) Image

```
kraft pkg --plat kraftcloud --arch x86_64 --name index.unikraft.io/"$UKC_USER"/resource-server:latest .
kraft pkg list --all
```

## Push Image

```
kraft pkg push index.unikraft.io/"$UKC_USER"/resource-server:latest
```

## List (Remote) Images

```
kraft cloud image list
```

## Create Instance

```
kraft cloud instance create -M 256M -V 1 -p 443:8080/tls+http --name resource-server index.unikraft.io/"$UKC_USER"/resource-server:latest
```
This creates an instance with 256 MiB memory and 1 vCPU. You can use a larger resource profile if needed, for example `-M 512M -V 2`.

## Start Instance

```
kraft cloud instance start resource-server
```

## List Instances

```
kraft cloud instance list
```

## Get Information about an Instance

```
kraft cloud instance get resource-server
kraft cloud instance get resource-server -o table
```

## Query Instance

```
fqdn=https://$(kraft cloud instance get resource-server -o json 2>/dev/null | jq -r '.data.instances[] | select(.name == "resource-server") | .service_group.domains[0].fqdn')
curl "$fqdn"
python3 test_resources.py "$fqdn"
```

## Get Instance Logs

```
kraft cloud instance logs resource-server
```

## Stop Instance

```
kraft cloud instance stop resource-server
```

## Delete Instance

```
kraft cloud instance delete resource-server
```

# Detailed Operations with the Unikraft Cloud Platform API

Below are detailed commands to deploy and operate instances with the Unikraft Cloud Platform API. The commands are scripts from the `api/` directory. These scripts make HTTP requests (via `curl`) to the REST API exposed by the platform.
Note: image-related operations do not directly interact with the platform API. Therefore, for creating and pushing images, the scripts use the `kraft` CLI tool, similarly to the CLI workflow.

## Create (Package) Image

```
./api/pkg-image.sh
```

## Push Image

```
./api/push-image.sh
```

## List (Remote) Images

```
./api/list-images.sh
```

## Create Instance

```
./api/create-instance.sh 256 1
```

This script is the core of the example. It creates an instance through the Unikraft Cloud Platform API and explicitly configures the instance resources in the request payload.

```
./api/create-instance.sh <memory_mb> <vcpus>
 
./api/create-instance.sh 256 1
./api/create-instance.sh 512 1
./api/create-instance.sh 512 2
```

The request payload includes `memory_mb` for memory allocation and `vcpus` for CPU allocation.

## Start Instance

```
./api/start-instance.sh
```

## List Instances

```
./api/list-instances.sh
```

## Get Information about an Instance

```
./api/get-instance-info.sh
```

## Query Instance

```
./api/query.sh
```

## Get Instance Logs

```
./api/get-instance-logs.sh
```

## Stop Instance

```
./api/stop-instance.sh
```

## Delete Instance

```
./api/delete-instance.sh
```
