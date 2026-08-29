# Distroless Django HTTP Server

This guide explains how to create and deploy a Python Django web app using a
**distroless** filesystem, built on top of
[`gcr.io/distroless/cc-debian12`](https://github.com/GoogleContainerTools/distroless)
instead of a hand-assembled `FROM scratch` image.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-python3.12-django5.0-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-python3.12-django5.0-distroless/
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
unikraft build . --output <my-org>/httpserver-python312-django50-distroless:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:80/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-python312-django50-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 1Gi \
  -p 443:80/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-python312-django50-distroless-vt56c
uuid:         d8469447-fdf6-4caf-9fea-494218ca6f72
state:        starting
image:        <my-org>/httpserver-python312-django50-distroless
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       109aa11f-da45-8d57-d5e4-6eb509ee3e73
  name:       dawn-sound-n5wrkxi2
  domains:
  - fqdn:     dawn-sound-n5wrkxi2.fra.unikraft.app
networks:
- uuid:       95f37ba4-2586-54a2-bf3e-5764c91c4fc1
  private-ip: 10.0.6.5
  mac:        12:b0:9c:af:65:e7
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-python312-django50-distroless-vt56c
 ├───────── uuid: d8469447-fdf6-4caf-9fea-494218ca6f72
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://dawn-sound-n5wrkxi2.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-python312-django50-distroless@sha256:221666d414299aff54dbf10020b3d540270ee0c5907c1c6a728ca254ce8b0e50
 ├─────── memory: 1024 MiB
 ├────── service: dawn-sound-n5wrkxi2
 ├─ private fqdn: httpserver-python312-django50-distroless-vt56c.internal
 └─── private ip: 10.0.6.5
```

In this case, the instance name is `httpserver-python312-django50-distroless-vt56c` and the address is `https://dawn-sound-n5wrkxi2.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Django web app server:

```bash
curl https://dawn-sound-n5wrkxi2.fra.unikraft.app
```

```html

<!doctype html>

<html lang="en-us" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>The install worked successfully! Congratulations!</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          html {
            line-height: 1.15;
          }
          a {
            color: #19865C;
          }
[...]
```

Or point a browser at the address and/or its `/admin` area.
You can set the username and password in the `Dockerfile.distroless` (more on this file later) to `unikraft/unikraft`.

> **Caution:**
> The example sets ALLOWED_HOSTS to * and runs in debug mode.
> For a production site, ensure you read the recommended deployment guides of the official Django project.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                             STATE    IMAGE                                               ARGS  MEMORY   VCPUS  FQDN                                  CREATED
fra    httpserver-python312-django50-distroless-vt56c  running  <my-org>/httpserver-python312-django50-distroless        1024MiB  1      dawn-sound-n5wrkxi2.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                             FQDN                                  STATE    STATUS        IMAGE                                                                            MEMORY    VCPUS  ARGS  BOOT TIME
httpserver-python312-django50-distroless-vt56c  dawn-sound-n5wrkxi2.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-python312-django50-distroless@sha256:...  1024 MiB  1            80.32 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances remove httpserver-python312-django50-distroless-vt56c
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-python312-django50-distroless-vt56c
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `main.py`: the entry point for the app
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem, built on a
  distroless base image

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/python3", "/app/main.py"]`: Use this as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM python:3.12-bookworm AS build`: A full Debian-based image used only
  to compile/install dependencies (`bjoern` ships a C extension, so a
  complete toolchain is required here). Nothing from this stage ends up in
  the final image except the files copied explicitly further down.

* `FROM gcr.io/distroless/cc-debian12`: The final, minimal runtime image.
  Unlike [`scratch`](https://hub.docker.com/_/scratch/), which starts
  completely empty, `distroless/cc-debian12` already ships a
  Google-maintained glibc runtime (`libc`, the dynamic linker,
  `libssl`/`libcrypto`, `libstdc++`, `ca-certificates`, `/etc/passwd`).
  Only what's specific to this app is copied on top: the Python 3.12
  interpreter and its standard library/site-packages, `libpython3.12.so.1.0`,
  and `libev`/`libsqlite3`/`libz`, none of which ship with the base
  distroless image.

The following options are available for customizing the app:

* If you only update the implementation in the `main.py` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).
  This includes the use of Python frameworks and the use of `pip`, as shown in the next section.

## Using `pip`

[`pip`](https://pip.pypa.io/en/stable/) is a package manager for Python.
It's used to install dependencies for Python apps.
`pip` uses the `requirements.txt` file to list required dependencies (with versions).

The [`httpserver-python3.12-flask3.0`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-python3.12-flask3.0) guide details the use of `pip` to deploy an app using the [`Flask`](https://flask.palletsprojects.com/en/3.0.x/) framework on Unikraft Cloud.

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