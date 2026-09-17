# Distroless Vite (vanilla)

This example demonstrates how to run a [Vite](https://vite.dev) project which
executes via the `vite` program on top of the `node` runtime.

> [!NOTE]
> This is **not** the most efficient way to run a Vite project! See
> [`httpserver-nginx-vite-vanilla`](../httpserver-nginx-vite-vanilla/) for more details.


## Initialization

The project was instantiated via:

```
npm create vite@latest my-vue-app -- --template vanilla
```

The accompanying `Dockerfile` and `Kraftfile` are
necessary for deploying to Unikraft Cloud.


## Deployment

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node-vite-vanilla-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node-vite-vanilla-distroless/
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

When done, run:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-node-vite-vanilla-distroless:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=2000,stateful=true \
  -e PWD=/app \
  --image <my-org>/httpserver-node-vite-vanilla-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 4Gi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 2s \
  -e PWD=/app \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-node-vite-vanilla-distroless-w9f3p
uuid:         4d5e6f7a-8b9c-0d1e-2f3a-d4e5f6a7b8c9
state:        starting
image:        <my-org>/httpserver-node-vite-vanilla-distroless
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       5e6f7a8b-9c0d-1e2f-3a4b-e5f6a7b8c9d0
  name:       bold-rain-mv5tx8wy
  domains:
  - fqdn:     bold-rain-mv5tx8wy.fra.unikraft.app
networks:
- uuid:       6f7a8b9c-0d1e-2f3a-4b5c-f6a7b8c9d0e1
  private-ip: 10.0.5.2
  mac:        12:b0:6c:3e:ab:95
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-node-vite-vanilla-distroless-w9f3p
 ├───────── uuid: 4d5e6f7a-8b9c-0d1e-2f3a-d4e5f6a7b8c9
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://bold-rain-mv5tx8wy.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-node-vite-vanilla-distroless@sha256:5a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b
 ├─────── memory: 4096 MiB
 ├────── service: bold-rain-mv5tx8wy
 ├─ private fqdn: httpserver-node-vite-vanilla-distroless-w9f3p.internal
 └─── private ip: 10.0.5.2
```

In this case, the instance name is `httpserver-node-vite-vanilla-distroless-w9f3p` and the address is `https://bold-rain-mv5tx8wy.fra.unikraft.app`.
They're different for each run.

After deploying, you can query the service using the provided URL.


You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                           STATE    IMAGE                                             ARGS  MEMORY   VCPUS  FQDN                                 CREATED
fra    httpserver-node-vite-vanilla-distroless-w9f3p  running  <my-org>/httpserver-node-vite-vanilla-distroless        4096MiB  1      bold-rain-mv5tx8wy.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                           FQDN                                 STATE    STATUS        IMAGE                                               MEMORY  VCPUS  ARGS  BOOT TIME
httpserver-node-vite-vanilla-distroless-w9f3p  bold-rain-mv5tx8wy.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-node-vite-vanilla-distroless@sha256:...  4 GiB   1            91.27 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete <instance-name>
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove <instance-name>
```


## Learn more

- [NGINX's Documentation](https://nginx.org/en/docs)
- [Vite's Documentation](https://vite.dev/guide/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs)
- [Building `Dockerfile` images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
- [Vite (vanilla) static build on Unikraft Cloud](../httpserver-nginx-vite-vanilla)
- [Vite (vanilla) SSR mode on Unikraft Cloud](../httpserver-node-vite-ssr-vanilla)


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
