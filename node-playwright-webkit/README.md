# Playwright (WebKit) with Node.js

[Playwright](https://playwright.dev/) is a framework for web testing and Automation.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node-playwright-webkit/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node-playwright-webkit/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/node-playwright-webkit:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/node-playwright-webkit:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         node-playwright-webkit-t7r2j
uuid:         a2b3c4d5-e6f7-8a9b-0c1d-a2b3c4d5e6f7
state:        starting
image:        <my-org>/node-playwright-webkit
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       b3c4d5e6-f7a8-9b0c-1d2e-b3c4d5e6f7a8
  name:       silent-fog-er8np3fb
  domains:
  - fqdn:     silent-fog-er8np3fb.fra.unikraft.app
networks:
- uuid:       c4d5e6f7-a8b9-0c1d-2e3f-c4d5e6f7a8b9
  private-ip: 10.0.6.4
  mac:        12:b0:a0:7c:ef:d9
timestamps:
  created:    just now
```

In this case, the instance name is `node-playwright-webkit-t7r2j` and the address is `https://silent-fog-er8np3fb.fra.unikraft.app`.
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

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                          STATE    IMAGE                            ARGS  MEMORY   VCPUS  FQDN                                  CREATED
fra    node-playwright-webkit-t7r2j  running  <my-org>/node-playwright-webkit        4096MiB  1      silent-fog-er8np3fb.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete <instance-name>
```

## Learn more

- [Playwright's Documentation](https://playwright.dev/docs/intro)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)


Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
