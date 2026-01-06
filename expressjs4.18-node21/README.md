# Node 21 Express

[Express](https://expressjs.com/) is a fast, unopinionated, minimalist web framework for Node.js.

This guide explains how to create and deploy an Express app.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/expressjs4.18-node21` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/expressjs4.18-node21/
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
 ├────── name: node21-expressjs-c34b9
 ├────── uuid: 15090da4-ac58-47e2-98d4-2c309b4b5274
 ├───── metro: fra
 ├───── state: running
 ├──── domain: https://holy-silence-vr9fp0zt.fra.unikraft.app
 ├───── image: node21-expressjs@sha256:f6082fe50fbb3b2659b445f5562b0d2040b4622112fdd1c8333ed10857d4ee27
 ├─ boot time: 131.91 ms
 ├──── memory: 512 MiB
 ├─── service: holy-silence-vr9fp0zt
 ├ private ip: 10.0.2.61
 └────── args: /usr/bin/node /usr/src/server.js
```

In this case, the instance name is `node21-expressjs-c34b9` and the address is `https://holy-silence-vr9fp0zt.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Express:

```bash
curl https://holy-silence-vr9fp0zt.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```

```ansi
NAME                    FQDN                                    STATE    STATUS   IMAGE                         MEMORY   VCPUS  ARGS                                 BOOT TIME
node21-expressjs-c34b9  holy-silence-vr9fp0zt.fra.unikraft.app  standby  standby  node21-expressjs@sha256:f...  512 MiB  1      /usr/bin/node /usr/src/server.js     131.03 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove node21-expressjs-c34b9
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `app/index.js`: the Express server program

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base-compat:latest`: The kernel to use.

* `rootfs: ./Dockerfile`: Build the app root filesystem using the `Dockerfile`.

* `cmd: ["/usr/bin/node", "/usr/src/server.js"]`: Use `/usr/bin/node /usr/src/server.js` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY ...`: Copy required files to the app filesystem: the `node` binary executable, libraries, configuration files, the `/usr/src/server.js` implementation.

* `RUN ...`: Run specific commands to generate or to prepare the filesystem contents.

The following options are available for customizing the app:

* If you want to replace `server.js` with a different source file, update the `cmd` line in the `Kraftfile` and replace `/usr/src/server.js` with the path to your new source file.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

- [Express's Documentation](https://expressjs.com/en/5x/api.html)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
