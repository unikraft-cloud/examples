# Distroless Express HTTP Server

[Express](https://expressjs.com/) is a fast, unopinionated, minimalist web framework for Node.js.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-expressjs4.18-node21-distroless` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-expressjs4.18-node21-distroless/
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
unikraft build . --output <my-org>/httpserver-expressjs418-node21-distroless:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-expressjs418-node21-distroless:latest
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
name:         httpserver-expressjs418-node21-distroless-lb3p2
uuid:         a1b2c3d4-e5f6-7890-abcd-ef1234567890
state:        starting
image:        <my-org>/httpserver-expressjs418-node21-distroless
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       aa081882-8173-7ea1-4136-aeee1d7d2316
  name:       calm-ocean-r9x4mk7v
  domains:
  - fqdn:     calm-ocean-r9x4mk7v.fra.unikraft.app
networks:
- uuid:       98ee012f-7acb-82f2-ddcb-7866393890a6
  private-ip: 10.0.3.4
  mac:        12:b0:97:42:f6:d9
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-expressjs418-node21-distroless-lb3p2
 ├───────── uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567890
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://calm-ocean-r9x4mk7v.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-expressjs418-node21-distroless@sha256:2e7d3f1a9c4b8e05d6f2a3b7c1e4d8f0a2b5c9e3d7f1a4b8
 ├─────── memory: 512 MiB
 ├────── service: calm-ocean-r9x4mk7v
 ├─ private fqdn: httpserver-expressjs418-node21-distroless-lb3p2.internal
 └─── private ip: 10.0.3.4
```

In this case, the instance name is `httpserver-expressjs418-node21-distroless-lb3p2` and the address is `https://calm-ocean-r9x4mk7v.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Express.js-based HTTP web server:

```bash
curl https://calm-ocean-r9x4mk7v.fra.unikraft.app
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
METRO  NAME                                             STATE    IMAGE                                               ARGS  MEMORY  VCPUS  FQDN                        CREATED
fra    httpserver-expressjs418-node21-distroless-lb3p2  running  <my-org>/httpserver-expressjs418-node21-distroless        512MiB  1      calm-ocean-r9x4mk7v.fra...  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                             FQDN                        STATE    STATUS       IMAGE                                            MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-expressjs418-node21-distroless-lb3p2  calm-ocean-r9x4mk7v.fra...  running  since 3mins  oci://unikraft.io/<my-org>/httpserver-expressjs418-node21-distroless@sha256:...  512 MiB  1            312.45 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-expressjs418-node21-distroless-lb3p2
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-expressjs418-node21-distroless-lb3p2
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `app/index.js`: the Express.js server implementation

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The kernel to use.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/node", "/usr/src/server.js"]`: Use `/usr/bin/node /usr/src/server.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM node:21-bookworm AS build`: Build the app using the Node.js 21 Bookworm (Debian 12) image.

* `COPY ...`: Copy required files to the app filesystem: the `node` binary executable, libraries, configuration files, and the Express.js app.

* `RUN npm install`: Install Express.js and other dependencies.

The following options are available for customizing the app:

* If you only update the implementation in the `app/index.js` source file, you don't need to make any other changes.

* If you want to add extra files, you need to copy them into the filesystem using the `COPY` command in the `Dockerfile`.

* If you want to replace `app/index.js` with a different source file, update the `cmd` line in the `Kraftfile` and replace `/usr/src/server.js` with the path to your new source file.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

- [Express's Documentation](https://expressjs.com/en/5x/api.html)
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
