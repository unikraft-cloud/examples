# Bun

This guide explains how to create and deploy a Bun app.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/bun` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/bun/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy the app on Unikraft Cloud:

```bash
kraft cloud deploy -p 443:3000 -M 512 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: bun-700mp
 ├────────── uuid: e467a880-075c-41e0-97ac-88e3e938523e
 ├───────── state: starting
 ├──────── domain: https://quiet-pond-ao44imcg.fra.unikraft.app
 ├───────── image: bun@sha256:dfcbee1efe0d8a1d43ab2dab70cf1cc5066bb1353aa1c528c745533d2cc33276
 ├──────── memory: 512 MiB
 ├─────── service: quiet-pond-ao44imcg
 ├── private fqdn: bun-700mp.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/bun run /usr/src/server.ts
```

In this case, the instance name is `bun-700mp` and the address is `https://quiet-pond-ao44imcg.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Bun instance:

```bash
curl https://quiet-pond-ao44imcg.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```

```ansi
NAME       FQDN                                  STATE    STATUS       IMAGE                               MEMORY   VCPUS  ARGS                                 BOOT TIME
bun-700mp  quiet-pond-ao44imcg.fra.unikraft.app  running  since 3mins  bun@sha256:dfcbee1efe0d8a1d43ab...  512 MiB  1      /usr/bin/bun run /usr/src/server.ts  289.03 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove bun-700mp
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `server.ts`: the Bun server implementation

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base-compat:latest`: The kernel to use.

* `rootfs: ./Dockerfile`: Build the app root filesystem using the `Dockerfile`.

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

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
