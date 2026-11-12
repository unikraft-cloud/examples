# Next.js HTTP Server

This guide explains how to create and deploy a Next.js app.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node21-nextjs` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node21-nextjs/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-node21-nextjs:latest
unikraft run --metro fra \
  -m 768M \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-node21-nextjs:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-node21-nextjs-bfrq0
uuid:         2adf9664-c4ae-4e0e-99de-c9781282b370
state:        starting
image:        <my-org>/httpserver-node21-nextjs
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

In this case, the instance name is `httpserver-node21-nextjs-bfrq0` and the address is `https://small-frog-ri8c1vtw.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Next.js server:

```bash
curl httpserver-node21-nextjs-bfrq0
```

```text
<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="preload" href="/_next/static/media/c9a5bc6a7c948fb0-s.p.woff2" ...
```

Or even better, point a browser at it 😀.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                            STATE    IMAGE                                     ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    httpserver-node21-nextjs-bfrq0  running  <my-org>/httpserver-node21-nextjs@sha256        768MiB  1      small-frog-ri8c1vtw.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-node21-nextjs-bfrq0
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `targets`: Build the app for the `kraftcloud/x86_64` and `kraftcloud/arm64` targets.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/local/bin/node", "/usr/src/server.js"]`: Use `/usr/local/bin/node /usr/src/server.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM node:21-alpine3.20 AS build`: Build the app using the Node.js 21 Alpine image of the target architecture.

* `RUN npm ci`: Install the dependencies at the versions in `package-lock.json`.

* `RUN npm run build`: Build the Next.js app as a standalone server in `.next/standalone`.

* `FROM node:21-alpine3.20 AS rootfs`: Prepare the app filesystem in a new stage of the same image.

* `RUN apk add --no-cache lddtree pax-utils`: Install `lddtree`, which finds the libraries that a binary needs.

* `COPY ...`: Copy the standalone server, the static files, and the `public` directory to `/usr/src`.

* `RUN ...`: Copy the `node` binary, the libraries that `node` and the native modules need, and `/usr/src` to `/rootfs`.
  Then make sure that `node` starts in `/rootfs` and loads the `sharp` native module.

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY --from=rootfs /rootfs /`: Copy the prepared files to the app filesystem.

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

Differences from the `http-node21` app are also the steps required to create an `npm`-based app:

1. Add the `package.json` and `package-lock.json` files used by `npm`.

2. Add framework-specific source files.
   In this case, this means the `app/` and `public/` directories and the Next.js configuration files.

3. Update the `Dockerfile` to:

   3.1. `RUN` the `npm ci` command to install dependencies.

   3.2. `RUN` the `npm run build` command to build the app.

   3.3. `COPY` the `node` binary, the libraries that it needs, and the build output to the app filesystem, using the [`scratch` container](https://hub.docker.com/_/scratch/).

The following lists the files:

The `package.json` file lists the `next`, `react`, and `react-dom` [dependencies](https://docs.npmjs.com/cli/v8/configuring-npm/package-json#dependencies).
The `package-lock.json` file pins the versions of all dependencies.
The `next.config.mjs` file sets `output: "standalone"`, so `npm run build` creates a standalone server in `.next/standalone`.

The `Kraftfile` is the same one used for `http-node21`.

For `Dockerfile` newly added lines have the following roles:

* `FROM node:21-alpine3.20 AS build`: Use the base image of the `node:21-alpine3.20` container for the target architecture.
  This provides the `npm` binary and other Node-related components.
  Name the current image `build`.

* `WORKDIR /usr/src`: Use `/usr/src` as working directory.
  All other commands in the `build` stage run inside this directory.

* `COPY package.json package-lock.json ./`: Copy the `npm` files to the Docker filesystem.

* `RUN npm ci`: Install the `npm` components at the versions listed in `package-lock.json`.

* `COPY . /usr/src/`: Copy the contents of the local current directory to the Docker filesystem.
  Note that paths in the `.dockerignore` file aren't copied.

* `RUN npm run build`: Build the Next.js app.

* `FROM node:21-alpine3.20 AS rootfs`: Prepare the app filesystem in a new stage of the same image.

* `COPY --from=build ...`: Copy the standalone server to `/usr/src` and the static files to `/usr/src/.next/static`.

* `RUN ...`: Copy the `node` binary, the libraries that `node` and the native modules in `node_modules/` need, and `/usr/src` to `/rootfs`.
  Then make sure that `node` starts in `/rootfs` and loads the `sharp` native module.

* `COPY --from=rootfs /rootfs /`: Copy the prepared files to the `scratch`-based image.

Similar actions apply to other `npm`-based apps.
See also other Node examples: [`httpserver-expressjs4.18-node21`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-expressjs4.18-node21) and [`httpserver-prisma-expressjs4.19-node18`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-prisma-expressjs4.19-node18).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
