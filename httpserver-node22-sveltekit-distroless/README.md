# Distroless SvelteKit HTTP Server

This guide explains how to create and deploy a [SvelteKit](https://kit.svelte.dev/) app.
[SvelteKit](https://kit.svelte.dev/) builds on Svelte, a UI framework that uses a compiler to let you write breathtakingly concise components that do minimal work in the browser.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node22-sveltekit-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node22-sveltekit-distroless/
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
unikraft build . --output <my-org>/httpserver-node22-sveltekit-distroless:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-node22-sveltekit-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 512Mi \
  -p 443:3000/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-node22-sveltekit-distroless-zmt39
uuid:         cd5071b0-5605-4771-b75d-4789393e60de
state:        starting
image:        <my-org>/httpserver-node22-sveltekit-distroless
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       2cd097b5-795c-7184-2968-1508c630fb2b
  name:       dark-fog-z18n0ej1
  domains:
  - fqdn:     dark-fog-z18n0ej1.fra.unikraft.app
networks:
- uuid:       e715723d-4659-2006-bd7b-68a5a3c33cce
  private-ip: 10.0.3.3
  mac:        12:b0:a0:31:90:5a
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-node22-sveltekit-distroless-zmt39
 ├───────── uuid: cd5071b0-5605-4771-b75d-4789393e60de
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://dark-fog-z18n0ej1.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-node22-sveltekit-distroless@sha256:4cea210aef3513bd68490640b511ebcff2b867e9222028b9938faccffc21cb83
 ├─────── memory: 512 MiB
 ├────── service: dark-fog-z18n0ej1
 ├─ private fqdn: httpserver-node22-sveltekit-distroless-zmt39.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `httpserver-node22-sveltekit-distroless-zmt39` and the address is `https://dark-fog-z18n0ej1.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance:

```bash
curl https://dark-fog-z18n0ej1.fra.unikraft.app
```

```text
<!doctype html>
<html lang="en">
[...]
        <body data-sveltekit-preload-data="hover">
[...]
```

Or even better, point a browser at it 😀
This will get you to play with the SvelteKit demo app.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                          STATE    IMAGE                                            ARGS  MEMORY  VCPUS  FQDN                                CREATED
fra    httpserver-node22-sveltekit-distroless-zmt39  running  <my-org>/httpserver-node22-sveltekit-distroless        512MiB  1      dark-fog-z18n0ej1.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                          FQDN                                STATE    STATUS         IMAGE                                              MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-node22-sveltekit-distroless-zmt39  dark-fog-z18n0ej1.fra.unikraft.app  running  5 minutes ago  oci://unikraft.io/<my-org>/httpserver-node22-sveltekit-distroless@sha256:...  512 MiB  1            72.86 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-node22-sveltekit-distroless-zmt39
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-node22-sveltekit-distroless-zmt39
```

## Customize your app

To customize the app, update the files in the repository.
That is, you update the SvelteKit / Node / `npm`-specific files, or the Unikraft Cloud-specific files.
This section details each below.

### Updating the app

Updating the SvelteKit app is reliant on making `npm`-related updates.

[`npm`](https://www.npmjs.com/) is a package manager for Node.
It's used to install dependencies for Node apps.
`npm` uses a `package.json` file to list required dependencies (with versions).

[`npm create svelte@latest`](https://kit.svelte.dev/docs/creating-a-project) generated the app files, using the [`@sveltejs/adapter-node`](https://kit.svelte.dev/docs/adapter-node) adapter.

The `src/routes/sverdle/` directory contains the core implementation.
Detailed information on updating the implementation is part of the [official SvelteKit documentation](https://kit.svelte.dev/docs/introduction).

Updates to the implementation will probably require updates to the `package.json` file.
The `package.json` file lists [`npm` app dependencies](https://docs.npmjs.com/cli/v8/configuring-npm/package-json#dependencies).

#### Deploying locally

Before deploying the SvelteKit app on Unikraft Cloud, you can deploy locally.
Assuming `npm` is installed, use the following commands:

```bash
npm install
npm run dev
```

```text
  VITE v5.2.6  ready in 807 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

You can test the app locally by pointing your browser to `http://localhost:5173/`.

### Sample specification

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: [["/nodejs/bin/node", "/app/build/index.js"]]`: Use `/nodejs/bin/node /app/build/index.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM node:22-bookworm AS base`: Use the base image of the `node:22-bookworm` container.
  This provides the `npm` binary and other Node-related components.
  Name the current image `base`.

* `WORKDIR /app`: Use `/app` as working directory.
  All other commands in the `Dockerfile` run inside this directory.

* `COPY package.json /app`: Copy the `npm` configuration file to be able to install dependencies.

* `RUN npm install`: Install `npm` components listed in `packages.json`.

* `FROM base AS build`: Create a fresh checkpoint of the base image for the build phase.

* `COPY . /app`: Copy contents of the current directory (the actual app files) in the Docker filesystem.
  Note that paths in the `.dockerignore` file aren't copied.

* `RUN npm run build; ...`: Build the files required for running the app standalone.
  The app entry point is the resulting `/app/build/index.js` file that's used as the start command in the `Kraftfile`.
  To run the app, configure it as a module.

* `FROM gcr.io/distroless/nodejs22-debian13:nonroot`: Use [the `FROM gcr.io/distroless/nodejs22-debian13` environment`](https://github.com/GoogleContainerTools/distroless/blob/main/nodejs/README.md) as the actual runtime environment.
  It will only contain the required files from the build and basic node22 dependencies.

* `COPY --from=build ...`: Copy existing files from new `build` image to the `gcr.io/distroless/nodejs22-debian13`-based image.
  This means the app build directory (`/app/build`) and the required dependencies (`/app/node_modules`).

#### Customization options

It's unlikely you will have to update the `Kraftfile`.
The only potential update is the `cmd` option.
But since SvelteKit / `npm` generates the `/app/build/index.js` file, you're unlikely to update it.

You also don't need to change the `Dockerfile`.
Updates to the app would be part of the `package.json` file or the `src/` directory.
And updating these won't affect the contents of the `Dockerfile`.
Still, if required, apps may require extending the `Dockerfile` with extra [`Dockerfile` commands](https://docs.docker.com/engine/reference/builder/).

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
