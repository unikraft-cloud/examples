# Distroless Node WebSocket Server

[WebSocket](https://en.wikipedia.org/wiki/WebSocket) is a bidirectional communication protocol over TCP, compatible with HTTP.
This example builds an echo-reply WebSocket server in [Node](https://nodejs.org/en).

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node21-websocket-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node21-websocket-distroless/
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
unikraft build . --output <my-org>/node21-websocket-distroless:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/node21-websocket-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --metro fra \
  -M 1Gi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         node21-websocket-distroless-j2x9r
uuid:         d5e6f7a8-b9c0-1d2e-3f4a-d5e6f7a8b9c0
state:        starting
image:        <my-org>/node21-websocket-distroless
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       e6f7a8b9-c0d1-2e3f-4a5b-e6f7a8b9c0d1
  name:       lively-breeze-hp3wx6yt
  domains:
  - fqdn:     lively-breeze-hp3wx6yt.fra.unikraft.app
networks:
- uuid:       f7a8b9c0-d1e2-3f4a-5b6c-f7a8b9c0d1e2
  private-ip: 10.0.5.4
  mac:        12:b0:d3:af:12:0c
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: node21-websocket-distroless-j2x9r
 ├───────── uuid: d5e6f7a8-b9c0-1d2e-3f4a-d5e6f7a8b9c0
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://lively-breeze-hp3wx6yt.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/node21-websocket-distroless@sha256:2b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c
 ├─────── memory: 1024 MiB
 ├────── service: lively-breeze-hp3wx6yt
 ├─ private fqdn: node21-websocket-distroless-j2x9r.internal
 └─── private ip: 10.0.5.4
```

In this case, the instance name is `node21-websocket-distroless-j2x9r` and the address is `https://lively-breeze-hp3wx6yt.fra.unikraft.app`.
They're different for each run.

The command will build the files in the current directory.

After deploying, you can query the service with a WebSocket client, such as [`wscat`](https://github.com/websockets/wscat).
Install `wscat` with `npm`:

```console
npm install -g wscat
```

Then query the WebSocket server deployed on Unikraft Cloud, using its URL:

```console
wscat --connect wss://<NAME>.<METRO>.unikraft.app
```

Then enter messages, that will be replied by the server.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                               STATE    IMAGE                                 ARGS  MEMORY   VCPUS  FQDN
              CREATED
fra    node21-websocket-distroless-j2x9r  running  <my-org>/node21-websocket-distroless        1024MiB  1      lively-breeze-hp3wx6yt.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                               FQDN                                     STATE    STATUS        IMAGE
                                        MEMORY   VCPUS  ARGS  BOOT TIME
node21-websocket-distroless-j2x9r  lively-breeze-hp3wx6yt.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/node21-websocket-distroless@sha256:...  1.0 GiB  1            45.83 ms
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

- [WebSocket documentation](https://nextjs.org/docs)
- [ws: A Node.js WebSocket library](https://github.com/websockets/ws)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)


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
