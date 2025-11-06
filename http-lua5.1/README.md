# Lua

This guide explains how to create and deploy a simple Lua-based HTTP web server.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-lua5.1/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-lua5.1/
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
kraft cloud deploy -p 443:8080 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: http-lua51-ma2i9
 ├────────── uuid: e7389eee-9808-4152-b2ec-1f3c0541fd05
 ├───────── state: running
 ├─────────── url: https://young-night-5fpf0jj8.fra.unikraft.app
 ├───────── image: http-lua51@sha256:278cb8b14f9faf9c2702dddd8bfb6124912d82c11b4a2c6590b6e32fc4049472
 ├───── boot time: 15.09 ms
 ├──────── memory: 128 MiB
 ├─────── service: young-night-5fpf0jj8
 ├── private fqdn: http-lua51-ma2i9.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/lua /http_server.lua
```

In this case, the instance name is `http-lua51-ma2i9` and the address is `https://young-night-5fpf0jj8.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Lua-based HTTP web server:

```bash
curl https://young-night-5fpf0jj8.fra.unikraft.app
```
```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME              FQDN                                   STATE    STATUS        IMAGE                                    MEMORY   VCPUS  ARGS                           BOOT TIME
http-lua51-ma2i9  young-night-5fpf0jj8.fra.unikraft.app  running  1 minute ago  http-lua51@sha256:278cb8b14f9faf9c27...  128 MiB  1      /usr/bin/lua /http_server.lua  15094us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-lua51-ma2i9
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `http_server.lua`: the actual Lua HTTP server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `http_server.lua` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
