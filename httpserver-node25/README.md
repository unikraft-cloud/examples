# Node HTTP Server

[Node.js](https://nodejs.org) is a free, open source, cross-platform JavaScript runtime environment.

To run this example, follow these steps:

1. Install the CLI and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node25` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-node25/
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

or

```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-node25:latest
unikraft run --metro fra -p 443:8080/tls+http -m 512M --image <my-org>/httpserver-node25:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:8080/tls+http -M 512M .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: httpserver-node25-v8mp4
 ├────────── uuid: c3d4e5f6-a7b8-9012-cdef-123456789012
 ├───────── state: starting
 ├──────── domain: https://bright-star-k3m7pqnx.fra.unikraft.app
 ├───────── image: httpserver-node25@sha256:7b3e1f9d5a2c8e4b0f6d3a7c5e2b9f4d1a8c6e3b0f7d4a1c8e5b2f9d6a3c0
 ├──────── memory: 512 MiB
 ├─────── service: bright-star-k3m7pqnx
 ├── private fqdn: httpserver-node25-v8mp4.internal
 ├──── private ip: 172.16.3.6
 └────────── args: /usr/bin/node /usr/src/server.js
```

In this case, the instance name is `httpserver-node25-v8mp4` and the address is `https://bright-star-k3m7pqnx.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Node.js HTTP server:

```bash
curl https://bright-star-k3m7pqnx.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

or

```bash title="kraft"
kraft cloud instance list
```

```ansi
NAME                     FQDN                                   STATE    STATUS       IMAGE                                 MEMORY   VCPUS  ARGS                              BOOT TIME
httpserver-node25-v8mp4  bright-star-k3m7pqnx.fra.unikraft.app  running  since 3mins  httpserver-node25@sha256:7b3e1f9d...  512 MiB  1      /usr/bin/node /usr/src/server.js  276.18 ms
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-node25-v8mp4
```

or

```bash title="kraft"
kraft cloud instance remove httpserver-node25-v8mp4
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `server.js`: the Node.js HTTP server implementation

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base-compat:latest`: The kernel to use.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `type: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/node", "/usr/src/server.js"]`: Use `/usr/bin/node /usr/src/server.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM node:25-alpine AS node`: Use the Node.js 25 Alpine image as the source for the `node` binary and libraries.

* `FROM scratch`: Build the runtime filesystem from a minimal base image.

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

```bash title="unikraft"
unikraft --help
```

or

```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
