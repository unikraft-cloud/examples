# Skipper

This example uses [`Skipper`](https://opensource.zalando.com/skipper/), an HTTP router and reverse proxy for service composition

To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/skipper/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/skipper/
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
kraft cloud deploy -p 443:9090 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: skipper-mx4ai
 ├────────── uuid: 34e3d740-c2b0-4644-b7e1-647350f688dc
 ├───────── state: running
 ├─────────── url: https://aged-sea-o7d3c42s.fra.unikraft.app
 ├───────── image: skipper@sha256:5483eaf3612cca2116ceaab9be42557686324f1d30337ae15d0495eef63d0386
 ├───── boot time: 43.71 ms
 ├──────── memory: 128 MiB
 ├─────── service: aged-sea-o7d3c42s
 ├── private fqdn: skipper-mx4ai.internal
 ├──── private ip: 172.16.6.4
 └────────── args: /usr/bin/skipper -address :9090 -routes-file /etc/skipper/example.eskip
```

In this case, the instance name is `skipper-mx4ai` and the address is `https://aged-sea-o7d3c42s.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Skipper.

```bash
curl https://aged-sea-o7d3c42s.fra.unikraft.app
```
```text
Hello, world from Skipper on Unikraft!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME           FQDN                                STATE    STATUS        IMAGE                      MEMORY   VCPUS  ARGS                                          BOOT TIME
skipper-mx4ai  aged-sea-o7d3c42s.fra.unikraft.app  running  1 minute ago  skipper@sha256:5483eaf...  128 MiB  1      /usr/bin/skipper -address :9090 -routes-f...  43709us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove skipper-mx4ai
```

## Customize your app

To customize Skipper you can change the `example.eskip` configuration file.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
