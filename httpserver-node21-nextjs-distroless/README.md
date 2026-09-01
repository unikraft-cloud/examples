# Distroless Next.js HTTP Server

This guide explains how to create and deploy a Next.js app.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node21-nextjs-distroless` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node21-nextjs-distroless/
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
unikraft build . --output <my-org>/httpserver-node21-nextjs-distroless:latest
unikraft run --metro fra \
  -m 768M \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-node21-nextjs-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 768Mi \
  -p 443:3000/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-node21-nextjs-distroless-bfrq0
uuid:         2adf9664-c4ae-4e0e-99de-c9781282b370
state:        starting
image:        <my-org>/httpserver-node21-nextjs-distroless
resources:
  memory:     768MiB
  vcpus:      1
service:
  uuid:       43e93d04-615b-0d81-07af-8506c25b1802
  name:       small-frog-ri8c1vtw
  domains:
  - fqdn:     small-frog-ri8c1vtw.fra.unikraft.app
networks:
- uuid:       e6e3adf9-8512-b678-4dae-6bbf2f4aad17
  private-ip: 10.0.28.2
  mac:        12:b0:2a:aa:d4:82
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-node21-nextjs-distroless-bfrq0
 ├───────── uuid: 2adf9664-c4ae-4e0e-99de-c9781282b370
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://small-frog-ri8c1vtw.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-node21-nextjs-distroless@sha256:ea5b2f145eea9762431ebdea933dd1dfb8427fe23306d2bd7966dd502d6c88f6
 ├─────── memory: 768 MiB
 ├────── service: small-frog-ri8c1vtw
 ├─ private fqdn: httpserver-node21-nextjs-distroless-bfrq0.internal
 └─── private ip: 10.0.28.2
```

In this case, the instance name is `httpserver-node21-nextjs-distroless-bfrq0` and the address is `https://small-frog-ri8c1vtw.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Next.js server:

```bash
curl httpserver-node21-nextjs-distroless-bfrq0
```

```text
<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="preload" href="/_next/static/media/c9a5bc6a7c948fb0-s.p.woff2" ...
```

Or even better, point a browser at it 😀.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                       STATE    IMAGE                                                ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    httpserver-node21-nextjs-distroless-bfrq0  running  <my-org>/httpserver-node21-nextjs-distroless@sha256        768MiB  1      small-frog-ri8c1vtw.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                       FQDN                                  STATE    STATUS        IMAGE                                          MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-node21-nextjs-distroless-bfrq0  small-frog-ri8c1vtw.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-node21-nextjs-distroless@sha256...  768 MiB  1            83.60 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-node21-nextjs-distroless-bfrq0
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-node21-nextjs-distroless-bfrq0
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: [["/usr/bin/node", "/usr/src/server.js"]]`: Use `/usr/bin/node /usr/src/server.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM gcr.io/distroless/cc-debian13:nonroot`: Build the filesystem from the [`gcr.io/distroless/cc-debian13` container image](https://github.com/GoogleContainerTools/distroless/blob/main/cc/README.md), to [create a base image](https://docs.docker.com/build/building/base-images/).

The following options are available for customizing the app:

* If you only update the implementation in the `server.js` source file, you don't need to make any other changes.

* If you want to add extra files, you need to copy them into the filesystem using the `COPY` command in the `Dockerfile`.

* If you want to replace `server.js` with a different source file, update the `cmd` line in the `Kraftfile` and replace `/usr/src/server.js` with the path to your new source file.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).
  This includes the use of Node frameworks and the use of [`npm`](https://www.npmjs.com/), as shown in the next section.

## Using `npm`

[`npm`](https://www.npmjs.com/) is a package manager for Node.
It's used to install dependencies for Node apps.
`npm` uses a `package.json` file to list required dependencies (with versions).

The [`httpserver-expressjs4.18-node21`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-expressjs4.18-node21) example in the [`examples`](https://github.com/unikraft-cloud/examples) repository details the use of `npm` to deploy an app using the [ExpressJS](https://expressjs.com/) framework on Unikraft Cloud.
Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `httpserver-expressjs4.18-node21` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-expressjs4.18-node21/
```

Run the command below to deploy the app on Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-expressjs418-node21:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-expressjs418-node21:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 256Mi \
  -p 443:3000/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  .
```

Differences from the `http-node21` app are also the steps required to create an `npm`-based app:

1. Add the `package.json` file used by `npm`.

2. Add framework-specific source files.
   In this case, this means `app/index.js`.

3. Update the `Dockerfile` to:

   3.1. `COPY` the local files.

   3.2. `RUN` the `npm install` command to install dependencies.

   3.3. `COPY` of the resulting and required files (`node_modules/` and `app/index.js`) in the app filesystem, using the [`scratch` container](https://hub.docker.com/_/scratch/).

The following lists the files:

The `package.json` file lists the `express` [dependency](https://docs.npmjs.com/cli/v8/configuring-npm/package-json#dependencies).

The `Kraftfile` is the same one used for `http-node21`.

For `Dockerfile` newly added lines have the following roles:

* `FROM node:21-bookworm AS build`: Use the base image of the `node:21-bookworm` container.
  This provides the `npm` binary and other Node-related components.
  Name the current image `build`.

* `WORKDIR /usr/src`: Use `/usr/src` as working directory.
  All other commands in the `Dockerfile` run inside this directory.

* `COPY . /usr/src/`: Copy the contents of the local current directory to the Docker filesystem.
  Note that paths in the `.dockerignore` file aren't copied.
  This means that `package.json` and `app/index.js` are copied.

* `RUN npm install`: Install `npm` components listed in `packages.json`.

* `COPY --from=build ...`: Copy existing files in the new `build` image in the `scratch`-based image.
  `/etc/os-release` must copy to provide the distribution information required by node.
  `/usr/src/node_modules` are the `npm`-generated files.
  `/usrc/src/app/index.js` is the original `ExpressJS` source code file.

Similar actions apply to other `npm`-based apps.
See also other Node examples: [`httpserver-node18-prisma-rest-express`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-node18-prisma-rest-express) and [`httpserver-node21-nextjs`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-node21-nextjs).

## Learn more

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
