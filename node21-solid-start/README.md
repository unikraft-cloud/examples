# SolidJS

This guide shows how to deploy a [Solid Start](https://start.solidjs.com) app.
To do so, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node21-solid-start/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/node21-solid-start/
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
 ├────────── name: node21-solid-start-lvoa2
 ├────────── uuid: 4e6ccb1f-0533-4dc1-be67-eca8dfc1f8c6
 ├───────── state: running
 ├─────────── url: https://long-star-1tms9h1z.fra.unikraft.app
 ├───────── image: node21-solid-start@sha256:eb2e79b2fc5c28bb43923a1fc4931db94ebc3f939a6fbe00d06189c0ae2e02fd
 ├───── boot time: 67.65 ms
 ├──────── memory: 256 MiB
 ├─────── service: long-star-1tms9h1z
 ├── private fqdn: node21-solid-start-lvoa2.internal
 ├──── private ip: 172.16.6.8
 └────────── args: /usr/bin/node /usr/src/server/index.mjs
```

In this case, the instance name is `node21-solid-start-lvoa2` and the address is `https://long-star-1tms9h1z.fra.unikraft.app`.
They're different for each run.
You can now point your browser at the address to see your deployed instance.

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME                      FQDN                                 STATE    STATUS         IMAGE          MEMORY   VCPUS  ARGS                              BOOT TIME
node21-solid-start-lvoa2  long-star-1tms9h1z.fra.unikraft.app  running  1 minutes ago  node21-sol...  256 MiB  1      /usr/bin/node /usr/src/server...  67.65 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove node21-solid-start-lvoa2
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `src/`: server source files

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
