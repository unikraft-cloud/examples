# Update Instance Command Line

This guide shows how to create an instance with an updated command line from the original image.

The guide explains how to do the above basic operations both using the [`unikraft` CLI](https://unikraft.com/docs/cli) and directly using the underlying [Unikraft Cloud platform API](https://unikraft.com/docs/api/platform/v1).

The target application we use in this guide is a simple C HTTP server.
There are two binary applications to be added in the image:
- `http_server`: a basic HTTP-reply server
- `http_server_args`: a basic HTTP-reply server that can receive as argument the message to be sent out

The image is built to use `/http_server` as the entry point / start command.
The guide demonstrates how start an instance that overrides the start command in the image with a new one: `/http_server_args "Bye, World!"`.

## Contents

The files used are:

- `http_server.c`: the simple C HTTP server app to be deployed on Unikraft Cloud
- `http_server_args.c`: the simple C HTTP server app to be deployed on Unikraft Cloud as an alternative binary, with an optional command line argument
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

## Use the Unikraft CLI

Below are the commands used to deploy and operate an instance with the [`unikraft` CLI](https://unikraft.com/docs/cli).
You can copy-paste them:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-c:latest
unikraft images list
unikraft run --metro fra --name httpserver-c -m 256M -p 443:8080/tls+http --image <my-org>/httpserver-c:latest
unikraft instances list
unikraft instances get httpserver-c
fqdn=https://$(unikraft instances get httpserver-c -o json | jq -r '.[0].service.domains[0].fqdn')
curl "$fqdn"
unikraft instances logs httpserver-c
unikraft instances stop httpserver-c
unikraft instances delete httpserver-c
unikraft instances list
unikraft run --metro fra --name httpserver-c -m 256M -p 443:8080/tls+http --image <my-org>/httpserver-c:latest --args '/http_server_args "Bye, World!"'
unikraft instances list
unikraft instances get httpserver-c
fqdn=https://$(unikraft instances get httpserver-c -o json | jq -r '.[0].service.domains[0].fqdn')
curl "$fqdn"
unikraft instances logs httpserver-c
unikraft instances stop httpserver-c
unikraft instances delete httpserver-c
```

In short, the above commands do the following:

1. Build and push the application image.
1. Create, query an delete an instance that uses the default command in the image: `/http_server`.
1. Create, query an delete an instance that uses an updated command, overriding the command in the image: `/http_server_args "Bye, World!"`.

The `--args` option replaces the command in the image.
The instance lists the new command in the `ARGS` column:

```ansi title="unikraft"
METRO  NAME          STATE    IMAGE                  ARGS                                  MEMORY  VCPUS  FQDN                                     CREATED
fra    httpserver-c  running  <my-org>/httpserver-c  ["/http_server_args", "Bye, World!"]  256MiB  1      sparkling-sun-ruy8eywy.fra.unikraft.app  just now
```

Commands are documented in the [`basic-ops/` guide](../basic-ops/).

## Use the Unikraft Cloud API

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
./api/create-instance-with-args.sh
./api/start-instance.sh
./api/query.sh
./api/get-instance-logs.sh
./api/stop-instance.sh
./api/delete-instance.sh
```

As in the previous section, the above commands do the following:

1. Build and push the application image.
1. Create, query an delete an instance that uses the default command in the image: `/http_server`.
1. Create, query an delete an instance that uses an updated command, overriding the command in the image: `/http_server_args "Bye, World!"`.

Commands are documented in the [`basic-ops/` guide](../basic-ops/).
