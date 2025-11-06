# Next.js

This guide explains how to create and deploy a Next.js app.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node21-nextjs` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/node21-nextjs/
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
kraft cloud deploy -p 443:3000 -M 256 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: node21-nextjs-bfrq0
 ├────────── uuid: 2adf9664-c4ae-4e0e-99de-c9781282b370
 ├───────── state: running
 ├─────────── url: https://small-frog-ri8c1vtw.fra.unikraft.app
 ├───────── image: node21-nextjs@sha256:ea5b2f145eea9762431ebdea933dd1dfb8427fe23306d2bd7966dd502d6c88f6
 ├───── boot time: 83.60 ms
 ├──────── memory: 256 MiB
 ├─────── service: small-frog-ri8c1vtw
 ├── private fqdn: node21-nextjs-bfrq0.internal
 ├──── private ip: 172.16.28.2
 └────────── args: /usr/bin/node /usr/src/server.js
```

In this case, the instance name is `node21-nextjs-bfrq0` and the address is `https://small-frog-ri8c1vtw.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Next.js server:

```bash
curl node21-nextjs-bfrq0
```
```text
<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="preload" href="/_next/static/media/c9a5bc6a7c948fb0-s.p.woff2" ...
```

Or even better, point a browser at it 😀.

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME                 FQDN                                  STATE    STATUS        IMAGE                    MEMORY   VCPUS  ARGS                              BOOT TIME
node21-nextjs-bfrq0  small-frog-ri8c1vtw.fra.unikraft.app  running  1 minute ago  node21-nextjs@sha256...  256 MiB  1      /usr/bin/node /usr/src/server.js  83600us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove node21-nextjs-bfrq0
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: node:21`: The Unikraft runtime kernel to use is Node 21.

* `rootfs: ./Dockerfile`: Build the app root filesystem using the `Dockerfile`.

* `cmd: [["/usr/bin/node", "/usr/src/server.js"]]`: Use `/usr/bin/node /usr/src/server.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

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

The [`node21-expressjs`](https://github.com/unikraft-cloud/examples/tree/main/node21-expressjs) example in the [`examples`](https://github.com/unikraft-cloud/examples) repository details the use of `npm` to deploy an app using the [ExpressJS](https://expressjs.com/) framework on Unikraft Cloud.
Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `node21-expressjs` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/node21-expressjs/
```

Run the command below to deploy the app on Unikraft Cloud:

```bash
kraft cloud deploy -p 443:3000 -M 256 .
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

* `FROM node:21-alpine AS build`: Use the base image of the `node:21-alpine` container.
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
See also other Node examples: [`node18-prisma-rest-express`](https://github.com/unikraft-cloud/examples/tree/main/node18-prisma-rest-express) and [`node21-nextjs`](https://github.com/unikraft-cloud/examples/tree/main/node21-nextjs).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
