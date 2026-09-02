# Distroless Ruby HTTP Server

This guide explains how to create and deploy a simple Ruby-based HTTP web server.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-ruby3.2-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-ruby3.2-distroless/
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
unikraft build . --output <my-org>/httpserver-ruby32-distroless:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-ruby32-distroless:latest
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
name:         httpserver-ruby32-distroless-s6l8n
uuid:         b1ebbbc0-5efa-476c-adb6-99866773245c
state:        starting
image:        <my-org>/httpserver-ruby32-distroless
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       bcc07c7c-9289-11f4-6e3d-8f7fdde45256
  name:       silent-resonance-1jtz5c66
  domains:
  - fqdn:     silent-resonance-1jtz5c66.fra.unikraft.app
networks:
- uuid:       50203783-cf51-81d1-aa2d-615f939043af
  private-ip: 10.0.3.3
  mac:        12:b0:0a:4f:7a:84
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-ruby32-distroless-s6l8n
 ├───────── uuid: b1ebbbc0-5efa-476c-adb6-99866773245c
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://silent-resonance-1jtz5c66.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-ruby32-distroless@sha256:4cf3b341898e6ebff18ff2b68353ef872dded650c9d16a6f005a8fbe8a7cbb3d
 ├─────── memory: 256 MiB
 ├────── service: silent-resonance-1jtz5c66
 ├─ private fqdn: httpserver-ruby32-distroless-s6l8n.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `httpserver-ruby32-distroless-s6l8n` and the address is `https://silent-resonance-1jtz5c66.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Ruby-based HTTP web server:

```bash
curl https://silent-resonance-1jtz5c66.fra.unikraft.app
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
METRO  NAME                                STATE    IMAGE                                  ARGS  MEMORY  VCPUS  FQDN                        CREATED
fra    httpserver-ruby32-distroless-s6l8n  running  <my-org>/httpserver-ruby32-distroless        256MiB  1      silent-resonance-1jtz5c66.fra.unikraf…  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                FQDN                                        STATE    STATUS          IMAGE                                    MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-ruby32-distroless-s6l8n  silent-resonance-1jtz5c66.fra.unikraft.app  running  12 minutes ago  oci://unikraft.io/<my-org>/httpserver-ruby32-dsitroless@sha256:...  256 MiB  1            71.19 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-ruby32-distroless-s6l8n
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-ruby32-distroless-s6l8n
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.rb`: the actual Ruby HTTP server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `server.rb` source file, you don't need to make any other changes.

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
