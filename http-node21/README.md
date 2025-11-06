# Node

This guide explains how to create and deploy a simple Node-based HTTP web server.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-node21/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-node21/
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
kraft cloud deploy -p 443:8080 -M 256 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: http-node21-ubl8g
 ├────────── uuid: 6985f8e7-72c2-4726-941c-3c568a83722e
 ├───────── state: running
 ├─────────── url: https://ancient-haze-sd3wwi0x.fra.unikraft.app
 ├───────── image: http-node21@sha256:de174e3703c79a048f0af52344c373296b55f3ca2b96cd29e16c1f014cefd232
 ├───── boot time: 41.65 ms
 ├──────── memory: 256 MiB
 ├─────── service: ancient-haze-sd3wwi0x
 ├── private fqdn: http-node21-ubl8g.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/node /usr/src/server.js
```

In this case, the instance name is `http-node21-ubl8g` and the address is `https://ancient-haze-sd3wwi0x.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Node-based HTTP web server:

```bash
curl https://ancient-haze-sd3wwi0x.fra.unikraft.app
```
```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME               FQDN                                    STATE    STATUS          IMAGE                                   MEMORY   VCPUS  ARGS                              BOOT TIME
http-node21-ubl8g  ancient-haze-sd3wwi0x.fra.unikraft.app  running  50 seconds ago  http-node21@sha256:de174e3703c79a04...  256 MiB  1      /usr/bin/node /usr/src/server.js  31654us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-node21-ubl8g
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.js`: the actual Node HTTP server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: node:21`: The Unikraft runtime kernel to use is Node 21.

* `rootfs: ./Dockerfile`: Build the app root filesystem using the `Dockerfile`.

* `cmd: ["/usr/bin/node", "/usr/src/server.js"]`: Use `/usr/bin/node /usr/src/server.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY ./server.js /usr/src/server.js`: Copy the server implementation file (`server.js`) in the Docker filesystem (in `/usr/src/server.js`).

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
