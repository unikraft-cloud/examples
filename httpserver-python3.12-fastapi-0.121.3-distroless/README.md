# Distroless FastAPI HTTP Server

This guide explains how to create and deploy a Python FastAPI web app.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

1. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-python3.12-fastapi-0.121.3-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-python3.12-fastapi-0.121.3-distroless/
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
unikraft build . --output <my-org>/httpserver-python312-fastapi-01213-distroless:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-python312-fastapi-01213-distroless:latest
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
name:         httpserver-python312-fastapi-01213-distroless-0n84f
uuid:         5d7fc331-3c23-4953-b025-d152a872ea29
state:        starting
image:        <my-org>/httpserver-python312-fastapi-01213-distroless
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       ced3df54-64cc-9217-3441-e0b4995319f0
  name:       dry-water-0oexx89g
  domains:
  - fqdn:     dry-water-0oexx89g.fra.unikraft.app
networks:
- uuid:       66d1766f-0a03-8b62-eb1a-0adb09b07b1d
  private-ip: 10.0.1.69
  mac:        12:b0:a1:15:7c:4a
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-python312-fastapi-01213-distroless-0n84f
 ├───────── uuid: 5d7fc331-3c23-4953-b025-d152a872ea29
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://dry-water-0oexx89g.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-python312-fastapi-01213-distroless@sha256:fb2a00dcf1cfc3ac821cbda05f82f38d66e63121344b9bc60c6a6e2f11917b98
 ├─────── memory: 512 MiB
 ├────── service: dry-water-0oexx89g
 ├─ private fqdn: httpserver-python312-fastapi-01213-distroless-0n84f.internal
 └─── private ip: 10.0.1.69
```

In this case, the instance name is `httpserver-python312-fastapi-01213-distroless-0n84f` and the address is `https://dry-water-0oexx89g.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Python FastAPI web app server:

```bash
curl https://dry-water-0oexx89g.fra.unikraft.app
```

```text
{"Hello":"World"}
```
You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                                 STATE    IMAGE                                                   ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    httpserver-python312-fastapi-01213-distroless-0n84f  standby  <my-org>/httpserver-python312-fastapi-01213-dsitroless        512MiB  1      dry-water-0oexx89g.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                                 FQDN                                 STATE    STATUS   IMAGE                                                   MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-python312-fastapi-01213-distroless-0n84f  dry-water-0oexx89g.fra.unikraft.app  standby  standby  oci://unikraft.io/<my-org>/httpserver-python312-fastapi-01213-distroless@sha25...  512 MiB  1            169.45 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances remove httpserver-python312-fastapi-01213-distroless-0n84f
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-python312-fastapi-01213-distroless-0n84f
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.py`: the entry point for the app
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The Unikraft runtime kernel to use is the latest that provides a minimal Linux-compatible environment.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/python3", "-m", "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080"]`: Use this as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM gcr.io/distroless/cc-debian12:latest`: Build the filesystem from the [`gcr.io/distroless/cc-debian12` container image](https://github.com/GoogleContainerTools/distroless/blob/main/cc/README.md), to [create a base image](https://docs.docker.com/build/building/base-images/).

The following options are available for customizing the app:

* If you only update the implementation in the `server.py` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

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
