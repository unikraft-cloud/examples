# Unikraft Cloud Basic Operations

This guide presents the basic operations when working with Unikraft Cloud instances and images.
Namely, it presents:

- deploying an instance (creating and starting it)
- building and pushing an image
- creating an instance
- starting an instance
- listing instances
- listing images
- getting information about an instance
- getting logs from an instance
- stopping an instance
- deleting an instance

The guide explains how to do the above basic operations both using the [`unikraft` CLI](https://unikraft.com/docs/cli) and directly using the underlying [Unikraft Cloud platform API](https://unikraft.com/docs/api/platform/v1).

The target application we use in this guide is a simple C HTTP server.

## Contents

The files used are:

- `http_server.c`: the simple C HTTP server app to be deployed on Unikraft Cloud
- `Dockerfile`: the Dockerfile to build the OCI (["Open Container Initiative"](https://opencontainers.org/)) image running the HTTP server app
- `Kraftfile`: the Unikraft Cloud specification file describing how to operate with the image (used by the `unikraft` CLI)
- `ukc.config.template`: a template configuration file for Unikraft Cloud
- `app.config`: the application configuration file for Unikraft Cloud
- `api/`: scripts used to directly interact with the [Unikraft Cloud platform API](https://unikraft.com/docs/api/platform/v1)
- `README.md` this file

## Prerequisites

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

## Set Up

Log into Unikraft Cloud:

```bash title="unikraft"
unikraft login
```

This guide uses the `fra` (Frankfurt, 🇩🇪) [metro](https://unikraft.com/docs/platform/metros).
Replace `<my-org>` in the commands below with your organization name.

To use the API scripts, create a `ukc.config` file as a copy of the `ukc.config.template`.
Replace the `TODO` entries in the `ukc.config` file with your corresponding Unikraft Cloud configuration values: user, token and metro.

## TLDR: Deploy and Operate an Instance

Below are the commands used to build an image and deploy and operate an instance (with the [`unikraft` CLI](https://unikraft.com/docs/cli)).
You can copy-paste them:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-c:latest
unikraft images list
unikraft run --metro fra --name httpserver-c -m 256M -p 443:8080/tls+http --image <my-org>/httpserver-c:latest
unikraft instances list
unikraft instances get httpserver-c
unikraft instances get httpserver-c -o table
fqdn=https://$(unikraft instances get httpserver-c -o json | jq -r '.[0].service.domains[0].fqdn')
curl "$fqdn"
unikraft instances logs httpserver-c
unikraft instances stop httpserver-c
sleep 2
unikraft instances start httpserver-c
unikraft instances delete httpserver-c
unikraft instances list
```

## TLDR: Pack and Push an Image and Operate an Instance via the API

Below are the commands used to deploy and operate an instance via the [Unikraft Cloud Platform API](https://unikraft.com/docs/api/platform/v1).
You can copy-paste them:

```console
./api/pkg-image.sh
./api/list-images.sh
./api/create-instance.sh
./api/start-instance.sh
./api/list-instances.sh
./api/get-instance-info.sh
./api/query.sh
./api/get-instance-logs.sh
./api/stop-instance.sh
./api/delete-instance.sh
./api/list-instances.sh
```

## Detailed Operations with the Unikraft CLI

Below are detailed commands to deploy and operate instances with the [`unikraft` CLI](https://unikraft.com/docs/cli).

### Build and Push Image

To build the image and push it to the Unikraft Cloud registry, use:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-c:latest
```

### List Images

To list remote images, use:

```bash title="unikraft"
unikraft images list
```

You will get an output similar to:

```ansi title="unikraft"
REF                    DIGEST
<my-org>/httpserver-c  sha256:9e5fa9887f36dfd5986d643f7cb1b84b865d35a31e618f453ead36ee44760098
```

### Deploy (Create and Start) Instance

> [!NOTE]
> We create an instance named `httpserver-c`.
> If a previous instance with the same name exists, you will get an error.
> You will have to delete the initial instance.

To create and start an instance (from an image), use:

```bash title="unikraft"
unikraft run --metro fra --name httpserver-c -m 256M -p 443:8080/tls+http --image <my-org>/httpserver-c:latest
```

Once the command completes, you will get an output of the running instance, similar to the one below:

```ansi title="unikraft"
metro:        fra
name:         httpserver-c
uuid:         ed4fbe82-f1a1-4b67-8564-a0050a72397e
state:        running
image:        <my-org>/httpserver-c@sha256:9e5fa9887f36dfd5986d643f7cb1b84b865d35a31e618f453ead36ee44760098
type:         micro
resources:
  memory:     256MiB
  vcpus:      1
service:
  name:       lingering-monkey-w6b1uun3
  uuid:       48264709-e8da-4088-b9d6-c545662311b2
  domains:
  - fqdn:     lingering-monkey-w6b1uun3.fra.unikraft.app
networks:
- uuid:       49b05b45-5bcd-4683-8df9-79d48a6e4391
  private-ip: 10.0.6.185
  mac:        12:b0:0a:00:06:b9
timestamps:
  created:    just now
timing:
  boot-time:  71.91ms
```

### Create and Start Instance Separately

To create an instance without starting it, use `unikraft instances create` with the same options:

```bash title="unikraft"
unikraft instances create --metro fra --name httpserver-c -m 256M -p 443:8080/tls+http --image <my-org>/httpserver-c:latest
```

The instance is in the `stopped` state.
To start it, use:

```bash title="unikraft"
unikraft instances start httpserver-c
```

### List Instances

To list all instances, use:

```bash title="unikraft"
unikraft instances list
```

You will get an output similar to:

```ansi title="unikraft"
METRO  NAME          STATE    IMAGE                  ARGS  MEMORY  VCPUS  FQDN                                        CREATED
fra    httpserver-c  running  <my-org>/httpserver-c        256MiB  1      lingering-monkey-w6b1uun3.fra.unikraft.app  just now
```

### Get Information about an Instance

To get information about an instance use:

```bash title="unikraft"
unikraft instances get httpserver-c
```

You will get the same output as the one printed when deploying the instance.

To list information about the instance in a simplified tabular format, use:

```bash title="unikraft"
unikraft instances get httpserver-c -o table
```

You will get an output similar to listing all instances:

```ansi title="unikraft"
METRO  NAME          STATE    IMAGE                  ARGS  MEMORY  VCPUS  FQDN                                        CREATED
fra    httpserver-c  running  <my-org>/httpserver-c        256MiB  1      lingering-monkey-w6b1uun3.fra.unikraft.app  just now
```

### Query Instance

To query the service exposed by the instance, use:

```bash title="unikraft"
fqdn=https://$(unikraft instances get httpserver-c -o json | jq -r '.[0].service.domains[0].fqdn')
curl "$fqdn"
```

You will get the "Hello, World!" message exposed by the service:

```text
Hello, World!
```

### Get Instance Logs

To get logging / printed information of the instance, use:

```bash title="unikraft"
unikraft instances logs httpserver-c
```

You will get an output similar to:

```ansi title="unikraft"
httpserver-c ┏ Listening on port 8080...
httpserver-c │ Sent a reply
```

### Stop Instance

```bash title="unikraft"
unikraft instances stop httpserver-c
```

#### Delete Instance

```bash title="unikraft"
unikraft instances delete httpserver-c
```

## Detailed Operations with the Unikraft Cloud Platform API

Below are detailed commands to deploy and operate instances with the [Unikraft Cloud Platform API](https://unikraft.com/docs/api/platform/v1).
The commands are scripts from the `api/` directory.
These scripts make HTTP requests (via `curl`) to the REST API exposed by the platform.

> [!NOTE]
> Image-related operations do not interact with the platform API.
> So, for building and pushing images, the scripts use the `unikraft` CLI, same as above.

### Build and Push Image

To build the image and push it to the Unikraft Cloud registry, use:

```console
./api/pkg-image.sh
```

### List (Remote) Images

To list remote images, use:

```console
./api/list-images.sh
```

You will get an output in JSON format similar to:

```text
[...]
      {
        "digest": "razvand/httpserver-c@sha256:7b467f0dcf7aaf271fdaa8c5282056d3e5d6d233e7d2e3cae2aea719d9a4a517",
        "tags": [
          "razvand/httpserver-c:latest"
        ],
        "initrd": true,
        "size_in_bytes": 39421724,
        "args": "/http_server"
      }
[...]
```

### Create Instance

> [!NOTE]
> We create an instance named `httpserver-c`.
> If a previous instance with the same name exists, you will get an error.
> You will have to delete the initial instance.

To create an instance (from an image), use:

```console
./api/create-instance.sh
```

You will get an output in JSON format similar to:

```json
{
  "status": "success",
  "data": {
    "instances": [
      {
        "status": "success",
        "uuid": "b053dffa-fc20-44ad-bb24-74c4451f7657",
        "name": "httpserver-c",
        "service_group": {
          "uuid": "0fe0c342-376c-4624-9cc1-b5092ed8bebf",
          "name": "cold-thunder-86wlirxf",
          "domains": [
            {
              "fqdn": "httpserver-c.sfo.unikraft.app"
            }
          ]
        },
        "private_ip": "10.0.0.197",
        "state": "stopped"
      }
    ]
  }
}
```

### Start Instance

To start an instance, use:

```console
./api/start-instance.sh
```

You will get an output in JSON format similar to:

```json
{
  "status": "success",
  "data": {
    "instances": [
      {
        "status": "success",
        "uuid": "b053dffa-fc20-44ad-bb24-74c4451f7657",
        "name": "httpserver-c",
        "previous_state": "stopped",
        "state": "starting"
      }
    ]
  }
}
```

### List Instances

```console
./api/list-instances.sh
```

You will get an output in JSON format similar to:

```text
{
  "status": "success",
  "data": {
    "instances": [
      {
        "uuid": "b053dffa-fc20-44ad-bb24-74c4451f7657",
        "name": "httpserver-c",
        "created_at": "2026-03-23T18:08:24Z",
        "state": "running",
        "image": "razvand/httpserver-c@sha256:7b467f0dcf7aaf271fdaa8c5282056d3e5d6d233e7d2e3cae2aea719d9a4a517",
        "memory_mb": 512,
        "vcpus": 1,
        "restart_policy": "never",
        "services": [
          "tcp:8080"
        ],
        "start_count": 1,
        "started_at": "2026-03-23T18:08:59Z",
        "uptime_ms": 18601,
        "boot_time_us": 150263,
        "net_time_us": 151070,
        "service_group": {
          "uuid": "0fe0c342-376c-4624-9cc1-b5092ed8bebf",
          "name": "cold-thunder-86wlirxf",
          "domains": [
            {
              "fqdn": "httpserver-c.sfo.unikraft.app"
            }
          ]
        },
        "network_interfaces": [
          {
            "uuid": "b56a3707-74d0-4399-b114-c39c1c9f323f",
            "private_ip": "10.0.0.197",
            "mac": "12:b0:0a:00:00:c5"
          }
        ],
        "private_ip": "10.0.0.197",
        "volumes": []
      }
    ]
  }
}
```

### Get Information about an Instance

```console
./api/get-instance-info.sh
```

You will get an output in JSON format similar to:

```text
{
  "status": "success",
  "data": {
    "instances": [
      {
        "status": "success",
        "uuid": "b053dffa-fc20-44ad-bb24-74c4451f7657",
        "name": "httpserver-c",
        "created_at": "2026-03-23T18:08:24Z",
        "state": "running",
        "image": "razvand/httpserver-c@sha256:7b467f0dcf7aaf271fdaa8c5282056d3e5d6d233e7d2e3cae2aea719d9a4a517",
        "memory_mb": 512,
        "vcpus": 1,
        "restart_policy": "never",
        "services": [
          "tcp:8080"
        ],
        "start_count": 1,
        "started_at": "2026-03-23T18:08:59Z",
        "uptime_ms": 36825,
        "boot_time_us": 150263,
        "net_time_us": 151070,
        "service_group": {
          "uuid": "0fe0c342-376c-4624-9cc1-b5092ed8bebf",
          "name": "cold-thunder-86wlirxf",
          "domains": [
            {
              "fqdn": "httpserver-c.sfo.unikraft.app"
            }
          ]
        },
        "network_interfaces": [
          {
            "uuid": "b56a3707-74d0-4399-b114-c39c1c9f323f",
            "private_ip": "10.0.0.197",
            "mac": "12:b0:0a:00:00:c5"
          }
        ],
        "private_ip": "10.0.0.197",
        "volumes": []
      }
    ]
  }
}
```

The output is similar to the command for listing instances, except that only the current instance is shown.

### Query Instance

```console
./api/query.sh
```

You will get the "Hello, World!" message exposed by the service:

```text
Hello, World!
```

### Get Instance Logs

```console
./api/get-instance-logs.sh
```

You will get an output similar to:

```text
Listening on port 8080...
Sent a reply
```

### Stop Instance

```console
./api/stop-instance.sh
```

You will get an output in JSON format similar to:

```text
{
  "status": "success",
  "data": {
    "instances": [
      {
        "status": "success",
        "uuid": "b053dffa-fc20-44ad-bb24-74c4451f7657",
        "name": "httpserver-c",
        "state": "stopping",
        "previous_state": "running"
      }
    ]
  }
}
```

#### Delete Instance

```console
./api/delete-instance.sh
```

You will get an output in JSON format similar to:

```text
{
  "status": "success",
  "data": {
    "instances": [
      {
        "status": "success",
        "uuid": "b053dffa-fc20-44ad-bb24-74c4451f7657",
        "name": "httpserver-c",
        "previous_state": "stopped"
      }
    ]
  }
}
```
