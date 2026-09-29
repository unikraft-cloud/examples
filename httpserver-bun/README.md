# Bun HTTP Server

This guide explains how to create and deploy a Bun app.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

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

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-bun:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-bun:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-bun-700mp
uuid:         e467a880-075c-41e0-97ac-88e3e938523e
state:        starting
image:        <my-org>/httpserver-bun
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       00cddace-e5e1-be6e-3423-86cccb5a1031
  name:       quiet-pond-ao44imcg
  domains:
  - fqdn:     quiet-pond-ao44imcg.fra.unikraft.app
networks:
- uuid:       3e41aab5-96c3-23e8-4afc-e2109f3f60de
  private-ip: 10.0.3.3
  mac:        12:b0:6e:91:eb:5a
timestamps:
  created:    just now
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

```ansi title="unikraft"
METRO  NAME                  STATE    IMAGE                    ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    httpserver-bun-700mp  running  <my-org>/httpserver-bun        512MiB  1      quiet-pond-ao44imcg.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-bun-700mp
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `server.ts`: the Bun server implementation

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The kernel to use.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

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

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
