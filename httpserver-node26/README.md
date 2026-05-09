# Node HTTP Server

[Node.js](https://nodejs.org) is a free, open source, cross-platform JavaScript runtime environment.

To run this example, follow these steps:

1. Install the CLI and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node26` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-node26/
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
unikraft build . --output <my-org>/httpserver-node26:latest
unikraft run --metro fra -p 443:8080/tls+http -m 512M --image <my-org>/httpserver-node26:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:8080/tls+http -M 512M .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────── name: httpserver-node26-ofwwl
 ├────── uuid: fa9d59d4-a935-41a6-bf29-9762fc0674f7
 ├───── metro: fra
 ├───── state: running
 ├──── domain: https://twilight-grass-hrjthti0.fra.unikraft.app
 ├───── image: httpserver-node26@sha256:942c611a1bcbc7d90812cfc830657aed82caf5f64ae4846ceaa982433ed32182
 ├─ boot time: 87.33 ms
 ├──── memory: 488 MiB
 ├─── service: twilight-grass-hrjthti0
 └ private ip: 10.0.10.9
```

In this case, the instance name is `httpserver-node26-ofwwl` and the address is `https://twilight-grass-hrjthti0.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Node.js HTTP server:

```bash
curl https://twilight-grass-hrjthti0.fra.unikraft.app
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
NAME                     FQDN         STAT  STAT  IMAG  MEMO  VCPU  ARGS  BOOT
httpserver-node26-ofwwl  twilight...  stan  stan  andr  488   1           87.9
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-node26-ofwwl
```

or

```bash title="kraft"
kraft cloud instance remove httpserver-node26-ofwwl
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
  `type: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/node", "/usr/src/server.js"]`: Use `/usr/bin/node /usr/src/server.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM node:26-alpine AS node`: Use the Node.js 26 Alpine image as the source for the `node` binary and libraries.

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
