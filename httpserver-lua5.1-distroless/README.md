# Distroless Lua HTTP Server

This guide explains how to create and deploy a simple Lua-based HTTP web server.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-lua5.1-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-lua5.1-distroless/
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
unikraft build . --output <my-org>/httpserver-lua51-distroless:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-lua51-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 256Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-lua51-distroless-ma2i9
uuid:         e7389eee-9808-4152-b2ec-1f3c0541fd05
state:        starting
image:        <my-org>/httpserver-lua51-distroless
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       51a41f63-7e88-c443-b9bf-83cd7c04d975
  name:       young-night-5fpf0jj8
  domains:
  - fqdn:     young-night-5fpf0jj8.fra.unikraft.app
networks:
- uuid:       afcc149e-cd07-a4b6-905a-6d498e251e14
  private-ip: 10.0.3.3
  mac:        12:b0:fe:e4:63:48
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-lua51-distroless-ma2i9
 ├───────── uuid: e7389eee-9808-4152-b2ec-1f3c0541fd05
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://young-night-5fpf0jj8.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-lua51-distroless@sha256:278cb8b14f9faf9c2702dddd8bfb6124912d82c11b4a2c6590b6e32fc4049472
 ├─────── memory: 256 MiB
 ├────── service: young-night-5fpf0jj8
 ├─ private fqdn: httpserver-lua51-distroless-ma2i9.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `httpserver-lua51-distroless-ma2i9` and the address is `https://young-night-5fpf0jj8.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Lua-based HTTP web server:

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
METRO  NAME                               STATE    IMAGE                                 ARGS  MEMORY  VCPUS  FQDN
     CREATED
fra    httpserver-lua51-distroless-ma2i9  running  <my-org>/httpserver-lua51-distroless        256MiB  1      young-night-5fpf0jj8.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                               FQDN                                   STATE    STATUS        IMAGE
                                        MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-lua51-distroless-ma2i9  young-night-5fpf0jj8.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-lua51-distroless@sha256:...  256 MiB  1            15.09 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-lua51-distroless-ma2i9
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-lua51-distroless-ma2i9
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `http_server.lua`: the actual Lua HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `http_server.lua` source file, you don't need to make any other changes.

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
