# Playwright (Chromium) with Node.js

[Playwright](https://playwright.dev/) is a framework for web testing and Automation.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node-playwright-chromium/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node-playwright-chromium/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/node-playwright-chromium:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/node-playwright-chromium:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         node-playwright-chromium-v5f8p
uuid:         a1b2c3d4-e5f6-7a8b-9c0d-a1b2c3d4e5f6
state:        starting
image:        <my-org>/node-playwright-chromium
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       b2c3d4e5-f6a7-8b9c-0d1e-b2c3d4e5f6a7
  name:       gentle-moon-cx2jh5wd
  domains:
  - fqdn:     gentle-moon-cx2jh5wd.fra.unikraft.app
networks:
- uuid:       c3d4e5f6-a7b8-9c0d-1e2f-c3d4e5f6a7b8
  private-ip: 10.0.4.3
  mac:        12:b0:8e:5a:cd:b7
timestamps:
  created:    just now
```

In this case, the instance name is `node-playwright-chromium-v5f8p` and the address is `https://gentle-moon-cx2jh5wd.fra.unikraft.app`.
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
METRO  NAME                            STATE    IMAGE                              ARGS  MEMORY   VCPUS  FQDN                                   CREATED
fra    node-playwright-chromium-v5f8p  running  <my-org>/node-playwright-chromium        4096MiB  1      gentle-moon-cx2jh5wd.fra.unikraft.app  2 minutes ago
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
