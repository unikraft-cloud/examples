# Ruby

This guide explains how to create and deploy a simple Ruby-based HTTP web server.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-ruby3.2/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-ruby3.2/
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
kraft cloud deploy -p 443:8080 -M 256 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: http-ruby32-s6l8n
 ├────────── uuid: b1ebbbc0-5efa-476c-adb6-99866773245c
 ├───────── state: running
 ├─────────── url: https://silent-resonance-1jtz5c66.fra.unikraft.app
 ├───────── image: http-ruby32@sha256:4cf3b341898e6ebff18ff2b68353ef872dded650c9d16a6f005a8fbe8a7cbb3d
 ├───── boot time: 71.19 ms
 ├──────── memory: 256 MiB
 ├─────── service: silent-resonance-1jtz5c66
 ├── private fqdn: http-ruby32-s6l8n.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/ruby /src/server.rb
```

In this case, the instance name is `http-ruby32-s6l8n` and the address is `https://silent-resonance-1jtz5c66.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Ruby-based HTTP web server:

```bash
curl https://silent-resonance-1jtz5c66.fra.unikraft.app
```
```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME               FQDN                                        STATE    STATUS          IMAGE                                                 MEMORY   VCPUS  ARGS                          BOOT TIME
http-ruby32-s6l8n  silent-resonance-1jtz5c66.fra.unikraft.app  running  12 minutes ago  http-ruby32@sha256:4cf3b341898e6ebff18ff2b68353ef...  256 MiB  1      /usr/bin/ruby /src/server.rb  71191us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-ruby32-s6l8n
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.rb`: the actual Ruby HTTP server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `server.rb` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
