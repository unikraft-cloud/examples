# MongoDB

This guide shows you how to use [MongoDB](https://www.mongodb.com), a source-available, cross-platform, document-oriented database program.

To run it, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/mongodb/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/mongodb/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash
kraft cloud deploy -p 27017:27017/tls -M 1024 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: mongodb-6tiuu
 ├────────── uuid: 99779597-0bdb-4160-b902-a160c3ab4b2a
 ├───────── state: running
 ├────────── fqdn: bold-brook-khkwv7of.fra.unikraft.app
 ├───────── image: mongodb@sha256:e6ff5153f106e2d5e2a10881818cd1b90fe3ff1294ad80879b2239ffc52aff0e
 ├───── boot time: 82.41 ms
 ├──────── memory: 1024 MiB
 ├─────── service: bold-brook-khkwv7of
 ├── private fqdn: mongodb-6tiuu.internal
 ├──── private ip: 172.16.6.4
 └────────── args: /usr/bin/mongod --bind_ip_all --nounixsocket
```

In this case, the instance name is `mongodb-6tiuu` which is different for each run.

To test the deployment, first forward the port with the `kraft cloud tunnel` command:

```bash
kraft cloud tunnel 27017:mongodb-6tiuu:27017
```

Then, on a separate console, you can use the `mongosh` client to connect to the server:
```console
mongosh mongodb://localhost
```

You should see output like:

```console
Current Mongosh Log ID: 65d75b96310f70e63565e0f1
Connecting to:  mongodb://localhost/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.5
(node:79750) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
(Use `node --trace-deprecation ...` to show where the warning was created)
Using MongoDB:  6.0.13
Using Mongosh:  2.1.5

For mongosh info see: https://docs.mongodb.com/mongodb-shell/

To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

test>
```

To disconnect, kill the `tunnel` command with `Ctrl+c`.

> **Note:**
> This guide uses `kraft cloud tunnel` only when a service doesn't support TLS and isn't HTTP-based (TLS/SNI determines the correct instance to send traffic to).
> Also note that the `tunnel` command isn't needed when connecting via an
> instance's private IP/FQDN.
> For example when a MongoDB instance serves as a database server to another instance that acts as a frontend and which **does** support TLS.

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME           FQDN                                  STATE    STATUS          IMAGE                             MEMORY   VCPUS  ARGS                              BOOT TIME
mongodb-6tiuu  bold-brook-khkwv7of.fra.unikraft.app  running  20 minutes ago  mongodb@sha256:e6ff5153f106e2...  1.0 GiB  1      /usr/bin/mongod --bind_ip_all...  82410us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove mongodb-6tiuu
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
