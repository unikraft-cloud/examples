# Distroless Python HTTP Server

This guide explains how to create and deploy a simple Python-based HTTP web server.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-python3.12-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-python3.12-distroless/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft login
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-python312-distroless:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-python312-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 512Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-python312-distroless-ma2i9
uuid:         e7389eee-9808-4152-b2ec-1f3c0541fd05
state:        starting
image:        <my-org>/httpserver-python312-distroless
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       51a41f63-7e88-c443-b9bf-83cd7c04d975
  name:       young-night-5fpf0jj8
  domains:
  - fqdn:     young-night-5fpf0jj8.fra.unikraft.app
networks:
- uuid:       53da3490-c6f5-3718-25f1-219a65163c73
  private-ip: 10.0.3.3
  mac:        12:b0:18:0c:cb:aa
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-python312-distroless-ma2i9
 ├───────── uuid: e7389eee-9808-4152-b2ec-1f3c0541fd05
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://young-night-5fpf0jj8.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-python312-distroless@sha256:278cb8b14f9faf9c2702dddd8bfb6124912d82c11b4a2c6590b6e32fc4049472
 ├─────── memory: 512 MiB
 ├────── service: young-night-5fpf0jj8
 ├─ private fqdn: httpserver-python312-distroless-ma2i9.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `httpserver-python312-distroless-ma2i9` and the address is `https://young-night-5fpf0jj8.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Python-based HTTP web server:

```bash
curl https://young-night-5fpf0jj8.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                   STATE    IMAGE                                     ARGS  MEMORY  VCPUS  FQDN                                   CREATED
fra    httpserver-python312-distroless-ma2i9  running  <my-org>/httpserver-python312-distroless        512MiB  1      young-night-5fpf0jj8.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                   FQDN                                   STATE    STATUS        IMAGE                                        MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-python312-distroless-ma2i9  young-night-5fpf0jj8.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-python312-distroless@sha256:...  512 MiB  1            15.09 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances remove httpserver-python312-distroless-ma2i9
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-python312-distroless-ma2i9
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.py`: the actual Python HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/python3", "/src/server.py"]`: Use `/usr/bin/python3 /src/server.py` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM gcr.io/distroless/python3-debian13:nonroot`: Build the filesystem from the [`gcr.io/distroless/python3-debian13` container image](https://github.com/GoogleContainerTools/distroless/tree/main/python3), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY ./server.py /src/server.py`: Copy the server implementation file (`server.py`) in the Docker filesystem (in `/src/server.py`).

The following options are available for customizing the app:

* If you only update the implementation in the `server.py` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).
  This includes the use of Python frameworks and the use of `pip`, as shown in the next section.

## Using `pip`

[`pip`](https://pip.pypa.io/en/stable/) is a package manager for Python.
It's used to install dependencies for Python apps.
`pip` uses the `requirements.txt` file to list required dependencies (with versions).

The [`httpserver-python3.12-flask3.0`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-python3.12-flask3.0) guide details the use of `pip` to deploy an app using the [`Flask`](https://flask.palletsprojects.com/en/3.0.x/) framework on Unikraft Cloud.

Run the command below to deploy the app on Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-python312-flask30:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-python312-flask30:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 512Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

Differences from the `httpserver-python3.12-flask3.0` app are also the steps required to create an `pip`-based app:

1. Add the `requirements.txt` file used by `pip`.

2. Add framework-specific source files.
   In this case, this means the `server.py` file.

3. Update the `Dockerfile` to:

   3.1. `COPY` the local files.

   3.2. `RUN` the `pip3 install` command to install dependencies.

   3.3. `COPY` of the resulting and required files (`/usr/local/lib/python3.12` and `server.py`) in the app filesystem, using the [`gcr.io/distroless/python3-debian13` container](https://hub.docker.com/_/scratch/).

The following lists the files:

The `requirements.txt` file lists the `flask` dependency.

The `Kraftfile` is the same one used for `httpserver-python3.12-flask3.0`.

For `Dockerfile` newly added lines have the following roles:

* `FROM python:3.13-slim-trixie AS builder`: Use the base image of the `python:3.13-slim-trixie` container.
  This provides the `pip3` binary and other Python-related components.
  Name the current image `builder`.

* `WORKDIR /src`: Use `/src` as working directory.
  All other commands in the `Dockerfile` run inside this directory.

* `COPY requirements.txt /src`: Copy the package configuration file to the Docker filesystem.

* `RUN pip3 install ...`: Install `pip` components listed in `requirements.txt`.

* `COPY --from=builder ...`: Copy generated Python files in the new `builder` image in the `gcr.io/distroless/python3-debian13`-based image.

Similar actions apply to other `pip3`-based apps.

See also the [`httpserver-python3.12-django5.0`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-python3.12-django5.0) example.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft --help
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
