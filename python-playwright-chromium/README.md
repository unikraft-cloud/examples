# Playwright (Chromium) with Python FastAPI

[Playwright](https://playwright.dev/) is a framework for web testing and Automation.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/python-playwright-chromium/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/python-playwright-chromium/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/python-playwright-chromium:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/python-playwright-chromium:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         python-playwright-chromium-m6k3p
uuid:         e6f7a8b9-c0d1-2e3f-4a5b-e6f7a8b9c0d1
state:        starting
image:        <my-org>/python-playwright-chromium
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       f7a8b9c0-d1e2-3f4a-5b6c-f7a8b9c0d1e2
  name:       young-night-kq8bv2mx
  domains:
  - fqdn:     young-night-kq8bv2mx.fra.unikraft.app
networks:
- uuid:       a8b9c0d1-e2f3-4a5b-6c7d-a8b9c0d1e2f3
  private-ip: 10.0.6.5
  mac:        12:b0:e4:b0:23:1d
timestamps:
  created:    just now
```

In this case, the instance name is `python-playwright-chromium-m6k3p` and the address is `https://young-night-kq8bv2mx.fra.unikraft.app`.
They're different for each run.

The command will deploy the files in the current directory.
It results in the creation of a remote web-based service for creating PNG screenshots of remote pages.

Use the `?page=<REMOTE_URL>` to point the service to the remote page to screenshot.
Query the service using commands such as:

```console
curl "https://<NAME>.<METRO>.unikraft.app/?page=https://google.com" -o ss-google.png
curl "https://<NAME>.<METRO>.unikraft.app/?page=https://github.com" -o ss-github.png
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                              STATE    IMAGE                                ARGS  MEMORY   VCPUS  FQDN                                   CREATED
fra    python-playwright-chromium-m6k3p  running  <my-org>/python-playwright-chromium        4096MiB  1      young-night-kq8bv2mx.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete <instance-name>
```

## Learn more

- [Playwright's Documentation](https://playwright.dev/docs/intro)
- [FastAPI's Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)


Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
