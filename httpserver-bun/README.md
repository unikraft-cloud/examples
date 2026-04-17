# Bun HTTP Server

This guide explains how to create and deploy a Bun app.
To run this example, follow these steps:

1. Install the CLI and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-bun` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-bun/
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
unikraft build . --output <my-org>/httpserver-bun:latest
unikraft run --metro fra -p 443:3000/tls+http -m 512M --image <my-org>/httpserver-bun:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:3000/tls+http -M 512M .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: httpserver-bun-700mp
 ├────────── uuid: e467a880-075c-41e0-97ac-88e3e938523e
 ├───────── state: starting
 ├──────── domain: https://quiet-pond-ao44imcg.fra.unikraft.app
 ├───────── image: httpserver-bun@sha256:dfcbee1efe0d8a1d43ab2dab70cf1cc5066bb1353aa1c528c745533d2cc33276
 ├──────── memory: 512 MiB
 ├─────── service: quiet-pond-ao44imcg
 ├── private fqdn: httpserver-bun-700mp.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/bun run /usr/src/server.ts
```

In this case, the instance name is `httpserver-bun-700mp` and the address is `https://quiet-pond-ao44imcg.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Bun HTTP web server:

```bash
curl https://quiet-pond-ao44imcg.fra.unikraft.app
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
NAME                  FQDN                                  STATE    STATUS       IMAGE                               MEMORY   VCPUS  ARGS                                 BOOT TIME
httpserver-bun-700mp  quiet-pond-ao44imcg.fra.unikraft.app  running  since 3mins  httpserver-bun@sha256:dfcbee1ef...  512 MiB  1      /usr/bin/bun run /usr/src/server.ts  289.03 ms
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-bun-700mp
```

or

```bash title="kraft"
kraft cloud instance remove httpserver-bun-700mp
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `server.ts`: the Bun server implementation

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base-compat:latest`: The kernel to use.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `type: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/bun", "run", "/usr/src/server.ts"]`: Use `/usr/bin/bun run /usr/src/server.ts` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY ...`: Copy required files to the app filesystem: the `bun` binary executable, libraries, configuration files, the `/usr/src/server.ts` implementation.

* `RUN ...`: Run specific commands to generate or to prepare the filesystem contents.

The following options are available for customizing the app:

* If you only update the implementation in the `server.ts` source file, you don't need to make any other changes.

* If you want to add extra files, you need to copy them into the filesystem using the `COPY` command in the `Dockerfile`.

* If you want to replace `server.ts` with a different source file, update the `cmd` line in the `Kraftfile` and replace `/usr/src/server.ts` with the path to your new source file.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

or

```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
