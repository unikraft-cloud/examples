# Distroless Playwright (Firefox) with Node.js

[Playwright](https://playwright.dev/) is a framework for web testing and Automation.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node-playwright-firefox-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node-playwright-firefox-distroless/
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
unikraft build . --output <my-org>/node-playwright-firefox-distroless:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/node-playwright-firefox-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 4Gi \
  -p 443:8080/tls+http \
  --scale-to-zero idle \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         node-playwright-firefox-distroless-q3m9k
uuid:         d4e5f6a7-b8c9-0d1e-2f3a-d4e5f6a7b8c9
state:        starting
image:        <my-org>/node-playwright-firefox-distroless
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       e5f6a7b8-c9d0-1e2f-3a4b-e5f6a7b8c9d0
  name:       bright-lake-dh6xp2sq
  domains:
  - fqdn:     bright-lake-dh6xp2sq.fra.unikraft.app
networks:
- uuid:       f6a7b8c9-d0e1-2f3a-4b5c-f6a7b8c9d0e1
  private-ip: 10.0.5.3
  mac:        12:b0:9f:6b:de:c8
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: node-playwright-firefox-distroless-q3m9k
 ├───────── uuid: d4e5f6a7-b8c9-0d1e-2f3a-d4e5f6a7b8c9
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://bright-lake-dh6xp2sq.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/node-playwright-firefox-distroless@sha256:8d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e
 ├─────── memory: 4096 MiB
 ├────── service: bright-lake-dh6xp2sq
 ├─ private fqdn: node-playwright-firefox-distroless-q3m9k.internal
 └─── private ip: 10.0.5.3
```

In this case, the instance name is `node-playwright-firefox-distroless-q3m9k` and the address is `https://bright-lake-dh6xp2sq.fra.unikraft.app`.
They're different for each run.

The command will deploy the files in the current directory.
It results in the creation of a remote web-based service for creating PNG screenshots of remote pages.

Use the `?page=<REMOTE_URL>` to point the service to the remote page to screenshot.
Query the service using commands such as:

```console
curl "https://<NAME>.<METRO>.unikraft.app/?page=https://google.com" -o ss-google.png
curl "https://<NAME>.<METRO>.unikraft.app/?page=https://bing.com" -o ss-bing.png
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                      STATE    IMAGE                                        ARGS  MEMORY   VCPUS
FQDN                                   CREATED
fra    node-playwright-firefox-distroless-q3m9k  running  <my-org>/node-playwright-firefox-distroless        4096MiB  1      bright-lake-dh6xp2sq.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                      FQDN                                   STATE    STATUS        IMAGE                                          MEMORY  VCPUS  ARGS  BOOT TIME
node-playwright-firefox-distroless-q3m9k  bright-lake-dh6xp2sq.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/node-playwright-firefox-distroless@sha256:...  4 GiB   1            350.87 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete <instance-name>
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove <instance-name>
```


## Learn more

- [Playwright's Documentation](https://playwright.dev/docs/intro)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)


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
