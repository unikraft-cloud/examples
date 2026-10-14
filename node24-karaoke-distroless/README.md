# Distroless Node AllKaraoke

[Allkaraoke](https://github.com/Asvarox/allkaraoke) offers an ultrastar deluxe-like online platform for karaoke.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node24-karaoke-distroless` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node24-karaoke-distroless/
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
unikraft build . --output <my-org>/node24-karaoke-distroless:latest
unikraft run --metro fra \
  -m 2G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=2000,stateful=true \
  --image <my-org>/node24-karaoke-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 2Gi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 2s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         node24-karaoke-distroless-9lw5q
uuid:         e5f6a7b8-c9d0-1234-efab-345678901234
state:        starting
image:        <my-org>/node24-karaoke-distroless
resources:
  memory:     2GiB
  vcpus:      1
service:
  uuid:       ef4112f8-10fc-fe6e-f48c-43a6623ec878
  name:       wild-song-p5q2nrwx
  domains:
  - fqdn:     wild-song-p5q2nrwx.fra.unikraft.app
networks:
- uuid:       cf5f3cbb-abf5-632e-3dd6-2de91885c6d9
  private-ip: 10.0.3.8
  mac:        12:b0:30:64:22:f9
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: node24-karaoke-distroless-9lw5q
 ├───────── uuid: e5f6a7b8-c9d0-1234-efab-345678901234
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://wild-song-p5q2nrwx.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/node24-karaoke-distroless@sha256:1a3c5e7b9d2f4a6c8e0b2d4f6a8c0e2b4d6f8a0b2c4e6f8a0b2d4f6a8c0e2b
 ├─────── memory: 2 GiB
 ├────── service: wild-song-p5q2nrwx
 ├─ private fqdn: node24-karaoke-distroless-9lw5q.internal
 └─── private ip: 10.0.3.8
```

In this case, the instance name is `node24-karaoke-distroless-9lw5q` and the address is `https://wild-song-p5q2nrwx.fra.unikraft.app`.
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

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                             STATE    IMAGE                               ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    node24-karaoke-distroless-9lw5q  running  <my-org>/node24-karaoke-distroless        2GiB    1      wild-song-p5q2nrwx.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                             FQDN                                 STATE    STATUS       IMAGE
                                      MEMORY  VCPUS  ARGS  BOOT TIME
node24-karaoke-distroless-9lw5q  wild-song-p5q2nrwx.fra.unikraft.app  running  since 3mins  oci://unikraft.io/<my-org>/node24-karaoke-distroless@sha256:...  2 GiB   1            1.24 s
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete node24-karaoke-distroless-9lw5q
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove node24-karaoke-distroless-9lw5q
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `entrypoint.sh`: the shell script used to start the AllKaraoke server

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The kernel to use.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/entrypoint.sh"]`: Use `/entrypoint.sh` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM node:24-bookworm-slim AS build`: Build the AllKaraoke project using the Node.js 24 Bookworm slim image.

* `RUN git clone ...; pnpm install; pnpm build`: Clone the AllKaraoke repository, install dependencies, and build it for production.

* `FROM gcr.io/distroless/nodejs24-debian12`: Use a fresh Node.js 24 Bookworm distroless image for the runtime.

* `COPY ...`: Copy required files to the app filesystem: the built AllKaraoke artifacts, and the entrypoint script.

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
