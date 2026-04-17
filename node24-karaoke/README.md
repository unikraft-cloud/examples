# Node AllKaraoke

[Allkaraoke](https://github.com/Asvarox/allkaraoke) offers an ultrastar deluxe-like online platform for karaoke.

To run this example, follow these steps:

1. Install the CLI and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node24-karaoke` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/node24-karaoke/
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
unikraft build . --output <my-org>/node24-karaoke:latest
unikraft run --metro fra -p 443:8080/tls+http -m 2G --image <my-org>/node24-karaoke:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:8080/tls+http -M 2G .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: node24-karaoke-9lw5q
 ├────────── uuid: e5f6a7b8-c9d0-1234-efab-345678901234
 ├───────── state: starting
 ├──────── domain: https://wild-song-p5q2nrwx.fra.unikraft.app
 ├───────── image: node24-karaoke@sha256:1a3c5e7b9d2f4a6c8e0b2d4f6a8c0e2b4d6f8a0b2c4e6f8a0b2d4f6a8c0e2b
 ├──────── memory: 2 GiB
 ├─────── service: wild-song-p5q2nrwx
 ├── private fqdn: node24-karaoke-9lw5q.internal
 ├──── private ip: 172.16.3.8
 └────────── args: /entrypoint.sh
```

In this case, the instance name is `node24-karaoke-9lw5q` and the address is `https://wild-song-p5q2nrwx.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the AllKaraoke instance:

```bash
curl https://wild-song-p5q2nrwx.fra.unikraft.app
```

```text
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AllKaraoke.Party - Free Online Karaoke</title>
    ...
  </head>
  ...
</html>
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
NAME                  FQDN                                 STATE    STATUS       IMAGE                                    MEMORY  VCPUS  ARGS            BOOT TIME
node24-karaoke-9lw5q  wild-song-p5q2nrwx.fra.unikraft.app  running  since 3mins  node24-karaoke@sha256:1a3c5e7b9d2f4a...  2 GiB   1      /entrypoint.sh  1.24 s
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete node24-karaoke-9lw5q
```

or

```bash title="kraft"
kraft cloud instance remove node24-karaoke-9lw5q
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `entrypoint.sh`: the shell script used to start the AllKaraoke server

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base-compat:latest`: The kernel to use.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `type: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/entrypoint.sh"]`: Use `/entrypoint.sh` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM node:24-bookworm-slim AS build`: Build the AllKaraoke project using the Node.js 24 Bookworm slim image.

* `RUN git clone ...; pnpm install; pnpm build`: Clone the AllKaraoke repository, install dependencies, and build it for production.

* `FROM node:24-bookworm-slim AS prod`: Use a fresh Node.js 24 Bookworm slim image for the runtime.

* `COPY ...`: Copy required files to the app filesystem: the `node` binary executable, system libraries, the built AllKaraoke artifacts, and the entrypoint script.

The following options are available for customizing the app:

* If you want to use a specific version of AllKaraoke, update the `git clone` command in the `Dockerfile` to pin a particular commit or tag.

* If you want to add extra files, you need to copy them into the filesystem using the `COPY` command in the `Dockerfile`.

* If you want to change the startup behavior, update the `entrypoint.sh` script.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

- [Allkaraoke official deployment](https://allkaraoke.party/)
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
