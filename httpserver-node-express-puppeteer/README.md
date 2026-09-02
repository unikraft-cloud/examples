# Headless Browsers: Puppeteer HTTP Server

Headless browsers power web scraping, automated testing, search engine optimization (SEO) rendering, screenshotting, and document generation.
They are resource-intensive and usually run in short bursts, which makes them a good fit for instances that boot in milliseconds and scale to zero between jobs.

This guide shows you how to use [Puppeteer](https://pptr.dev/), a Node.js library which provides a high-level API to control browsers, including the option to run them headless (no UI).
The example wraps Puppeteer in an [Express](https://expressjs.com/) HTTP server that renders a URL or an HTML payload to PDF.

To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-node-express-puppeteer/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-node-express-puppeteer/
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

The `UKC_TOKEN` and `UKC_METRO` environment variables are only supported by the legacy CLI.


> **Note:**
> A Puppeteer instance on Unikraft Cloud requires 4GB to run.
> Request an increase in the instance memory quota when you need more memory.

When done, invoke the following command to deploy this app on Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-node-express-puppeteer:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:3000/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-node-express-puppeteer:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 4Gi \
  -p 443:3000/tls+http \
  --scale-to-zero idle \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-node-express-puppeteer-7afg3
uuid:         7bb479d7-5b3e-444f-b07c-eae4da6f57cc
state:        starting
image:        <my-org>/httpserver-node-express-puppeteer
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       996b9cc1-5a51-e707-d443-5c98ea86ded8
  name:       little-snow-7qwu6vv5
  domains:
  - fqdn:     little-snow-7qwu6vv5.fra.unikraft.app
networks:
- uuid:       034fa25e-9154-7842-ccdd-289256cc7a17
  private-ip: 10.0.3.1
  mac:        12:b0:8f:3c:f5:16
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-node-express-puppeteer-7afg3
 ├───────── uuid: 7bb479d7-5b3e-444f-b07c-eae4da6f57cc
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://nameless-fog-0tvh1uov.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-node-express-puppeteer@sha256:78d0b180161c876f17d05116b93011ddcd44c76758d6fa0359f05938e67cea65
 ├─────── memory: 4096 MiB
 ├────── service: little-snow-7qwu6vv5
 ├─ private fqdn: httpserver-node-express-puppeteer-7afg3.internal
 └─── private ip: 10.0.3.1
```

In this case, the instance name is `httpserver-node-express-puppeteer-7afg3`.
They're different for each run.

Use a browser to access the landing page of the Puppeteer (that uses [ExpressJS](https://expressjs.com/)).
The app and the landing page are part of [this repository](https://github.com/christopher-talke/node-express-puppeteer-pdf-example).

In the example run above the landing page is at `https://nameless-fog-0tvh1uov.fra.unikraft.app`.
You can use the landing page to generate the PDF version of a remote page.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                     STATE    IMAGE                                       ARGS  MEMORY   VCPUS  FQDN                                    CREATED
fra    httpserver-node-express-puppeteer-7afg3  running  <my-org>/httpserver-node-express-puppeteer        4096MiB  1      nameless-fog-0tvh1uov.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                     FQDN                                    STATE    STATUS       IMAGE                                                              MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-node-express-puppeteer-7afg3  nameless-fog-0tvh1uov.fra.unikraft.app  running  since 6mins  oci://unikraft.io/<my-org>/httpserver-node-express-puppeteer@s...  4.0 GiB  1            15.27 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-node-express-puppeteer-7afg3
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-node-express-puppeteer-7afg3
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

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview) or the [legacy CLI Reference](https://unikraft.com/docs/cli/overview).
