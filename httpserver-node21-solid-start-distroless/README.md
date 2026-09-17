# Distroless SolidJS HTTP Server

This guide shows how to deploy a [Solid Start](https://start.solidjs.com) app.
To do so, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node21-solid-start-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node21-solid-start-distroless/
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
unikraft build . --output <my-org>/httpserver-node21-solid-start-distroless:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-node21-solid-start-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 512Mi \
  -p 443:3000/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-node21-solid-start-distroless-lvoa2
uuid:         4e6ccb1f-0533-4dc1-be67-eca8dfc1f8c6
state:        starting
image:        <my-org>/httpserver-node21-solid-start-distroless
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       46865b94-fd59-7d38-485d-c110a41b0949
  name:       long-star-1tms9h1z
  domains:
  - fqdn:     long-star-1tms9h1z.fra.unikraft.app
networks:
- uuid:       1b8eccba-a635-e4db-3a3f-162fbe1f692f
  private-ip: 10.0.6.8
  mac:        12:b0:8e:29:47:83
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-node21-solid-start-distroless-lvoa2
 ├───────── uuid: 4e6ccb1f-0533-4dc1-be67-eca8dfc1f8c6
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://long-star-1tms9h1z.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-node21-solid-start-distroless@sha256:eb2e79b2fc5c28bb43923a1fc4931db94ebc3f939a6fbe00d06189c0ae2e02fd
 ├─────── memory: 512 MiB
 ├────── service: long-star-1tms9h1z
 ├─ private fqdn: httpserver-node21-solid-start-distroless-lvoa2.internal
 └─── private ip: 10.0.6.8
```

In this case, the instance name is `httpserver-node21-solid-start-distroless-lvoa2` and the address is `https://long-star-1tms9h1z.fra.unikraft.app`.
They're different for each run.
You can now point your browser at the address to see your deployed instance.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                            STATE    IMAGE                                              ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    httpserver-node21-solid-start-distroless-lvoa2  running  <my-org>/httpserver-node21-solid-start-distroless        512MiB  1      long-star-1tms9h1z.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                            FQDN                                 STATE    STATUS         IMAGE                                               MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-node21-solid-start-distroless-lvoa2  long-star-1tms9h1z.fra.unikraft.app  running  1 minutes ago  oci://unikraft.io/<my-org>/httpserver-node21-solid-start-distroless@sha256...  512 MiB  1            67.65 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-node21-solid-start-distroless-lvoa2
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-node21-solid-start-distroless-lvoa2
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `src/`: server source files

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
