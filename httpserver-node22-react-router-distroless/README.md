# React Router HTTP Server

This guide shows how to deploy a [React Router](https://reactrouter.com/) app (formerly Remix).

To do so, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node22-react-router-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node22-react-router-distroless/
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
unikraft build . --output <my-org>/httpserver-node22-react-router-distroless:latest
unikraft run --metro fra \
  -m 768M \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-node22-react-router-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 768Mi \
  -p 443:3000/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-node22-react-router-distroless-jvj6b
uuid:         4e6ccb1f-0533-4dc1-be67-eca8dfc1f8c6
state:        starting
image:        <my-org>/httpserver-node22-react-router-distroless
resources:
  memory:     768MiB
  vcpus:      1
service:
  uuid:       46865b94-fd59-7d38-485d-c110a41b0949
  name:       long-star-1tms9h1z
  domains:
  - fqdn:     long-star-1tms9h1z.fra.unikraft.app
networks:
- uuid:       270bdb2f-42a2-f26d-4a8c-43de55608490
  private-ip: 10.0.6.8
  mac:        12:b0:00:61:6e:70
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-node22-react-router-distroless-jvj6b
 ├───────── uuid: 4e6ccb1f-0533-4dc1-be67-eca8dfc1f8c6
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://long-star-1tms9h1z.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-node22-react-router-distroless@sha256:300eefce3de136ad9c782f010b69da01100ae5f0ca17f038f92321d735d6675f
 ├─────── memory: 768 MiB
 ├────── service: long-star-1tms9h1z
 ├─ private fqdn: httpserver-node22-react-router-distroless-jvj6b.internal
 └─── private ip: 10.0.6.8
```

In this case, the instance name is `httpserver-node22-react-router-distroless-jvj6b` and the address is `https://long-star-1tms9h1z.fra.unikraft.app`.
They're different for each run.
You can now point your browser at the address to see your deployed instance.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                             STATE    IMAGE                                               ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    httpserver-node22-react-router-distroless-jvj6b  running  <my-org>/httpserver-node22-react-router-distroless        768MiB  1      long-star-1tms9h1z.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                             FQDN                                 STATE    STATUS         IMAGE                                                MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-node22-react-router-distroless-jvj6b  long-star-1tms9h1z.fra.unikraft.app  running  1 minutes ago  oci://unikraft.io/<my-org>/httpserver-node22-react-router-distroless@sha256...  768 MiB  1            67.65 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-node22-react-router-distroless-jvj6b
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-node22-react-router-distroless-jvj6b
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `server.js`: the server itself

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
