# Distroless Node HTTP Server

[Node.js](https://nodejs.org) is a free, open source, cross-platform JavaScript runtime environment.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node26-distroless` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node26-distroless/
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
unikraft build . --output <my-org>/httpserver-node26-distroless:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-node26:latest
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
name:         httpserver-node26-distroless-v8mp4
uuid:         c3d4e5f6-a7b8-9012-cdef-123456789012
state:        starting
image:        <my-org>/httpserver-node26-distroless
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       8c6367b6-d913-4b24-fbc4-922cf124c8f8
  name:       bright-star-k3m7pqnx
  domains:
  - fqdn:     bright-star-k3m7pqnx.fra.unikraft.app
networks:
- uuid:       229c5467-216f-79dd-e2f9-3307b196fad3
  private-ip: 10.0.3.6
  mac:        12:b0:25:ce:7f:75
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-node26-distroless-v8mp4
 ├───────── uuid: c3d4e5f6-a7b8-9012-cdef-123456789012
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://bright-star-k3m7pqnx.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-node26-distroless@sha256:7b3e1f9d5a2c8e4b0f6d3a7c5e2b9f4d1a8c6e3b0f7d4a1c8e5b2f9d6a3c0
 ├─────── memory: 512 MiB
 ├────── service: bright-star-k3m7pqnx
 ├─ private fqdn: httpserver-node26-distroless-v8mp4.internal
 └─── private ip: 10.0.3.6
```

In this case, the instance name is `httpserver-node26-distroless-v8mp4` and the address is `https://bright-star-k3m7pqnx.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Node.js HTTP server:

```bash
curl https://bright-star-k3m7pqnx.fra.unikraft.app
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
METRO  NAME                                STATE    IMAGE                                  ARGS  MEMORY  VCPUS FQDN                               CREATED
fra    httpserver-node26-distroless-v8mp4  running  <my-org>/httpserver-node26-distroless        512MiB  1      bright-star-k3m7pqnx.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                FQDN                                   STATE    STATUS       IMAGE
                       MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-node26-distroless-v8mp4  bright-star-k3m7pqnx.fra.unikraft.app  running  since 3mins  oci://unikraft.io/<my-org>/httpserver-node26-distroless@sha256:...  512 MiB  1            276.18 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-node26-distroless-v8mp4
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-node26-distroless-v8mp4
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `server.js`: the Node.js HTTP server implementation

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The kernel to use.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/node", "/usr/src/server.js"]`: Use `/usr/bin/node /usr/src/server.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM nvitaterna/nodejs-distroless:26`: Built runtime for node26 applications.

* `COPY ...`: Copy required files to the app filesystem: the `node` binary executable, libraries, and the `/usr/src/server.js` implementation.

The following options are available for customizing the app:

* If you only update the implementation in the `server.js` source file, you don't need to make any other changes.

* If you want to add extra files, you need to copy them into the filesystem using the `COPY` command in the `Dockerfile`.

* If you want to replace `server.js` with a different source file, update the `cmd` line in the `Kraftfile` and replace `/usr/src/server.js` with the path to your new source file.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

- [Node.js's Documentation](https://nodejs.org/docs/latest/api/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)


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
