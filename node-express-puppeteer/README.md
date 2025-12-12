# Puppeteer

This guide shows you how to use [Puppeteer](https://pptr.dev/), a Node.js library which provides a high-level API to control browsers, including the option to run them headless (no UI).

To run it, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node-express-puppeteer/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/node-express-puppeteer/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

> **Note:**
> A Puppeteer instance on Unikraft Cloud requires 4GB to run.
> Request an increase in the instance memory quota when you need more memory.

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash
kraft cloud deploy -p 443:3000 -M 4096 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: node-express-puppeteer-7afg3
 ├────────── uuid: 7bb479d7-5b3e-444f-b07c-eae4da6f57cc
 ├───────── state: starting
 ├──────── domain: https://nameless-fog-0tvh1uov.fra.unikraft.app
 ├───────── image: node-express-puppeteer@sha256:78d0b180161c876f17d05116b93011ddcd44c76758d6fa0359f05938e67cea65
 ├──────── memory: 4096 MiB
 ├─────── service: little-snow-7qwu6vv5
 ├── private fqdn: node-express-puppeteer-7afg3.internal
 ├──── private ip: 172.16.3.1
 └────────── args: /usr/bin/wrapper.sh /usr/bin/node /app/bin/www
```

In this case, the instance name is `node-express-puppeteer-7afg3`.
They're different for each run.

Use a browser to access the landing page of the Puppeteer (that uses [ExpressJS](https://expressjs.com/)).
The app and the landing page are part of [this repository](https://github.com/christopher-talke/node-express-puppeteer-pdf-example).

In the example run above the landing page is at `https://nameless-fog-0tvh1uov.fra.unikraft.app`.
You can use the landing page to generate the PDF version of a remote page.

You can list information about the instance by running:

```bash
kraft cloud instance list node-express-puppeteer-7afg3
```

```ansi
NAME                          FQDN                                    STATE    STATUS       IMAGE                        MEMORY   VCPUS  ARGS                               BOOT TIME
node-express-puppeteer-7afg3  nameless-fog-0tvh1uov.fra.unikraft.app  running  since 6mins  node-express-puppeteer@s...  4.0 GiB  1      /usr/bin/wrapper.sh /usr/bin/n...  15.27 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove node-express-puppeteer-7afg3
```

## Customize your deployment

The current deployment uses an ExpressJS service that uses the [PDF generating functionality of Puppeteer](https://devdocs.io/puppeteer/).
Customizing the deployment means updating the service, such as adding new functionalities provided by Puppeteer.
You can update the service to provide a REST-like interface.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
