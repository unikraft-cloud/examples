# Playwright (Firefox) with Node.js

[Playwright](https://playwright.dev/) is a framework for web testing and Automation.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/node-playwright-firefox/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/node-playwright-firefox/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/node-playwright-firefox:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/node-playwright-firefox:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         node-playwright-firefox-q3m9k
uuid:         d4e5f6a7-b8c9-0d1e-2f3a-d4e5f6a7b8c9
state:        starting
image:        <my-org>/node-playwright-firefox
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

In this case, the instance name is `node-playwright-firefox-q3m9k` and the address is `https://bright-lake-dh6xp2sq.fra.unikraft.app`.
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
METRO  NAME                           STATE    IMAGE                             ARGS  MEMORY   VCPUS  FQDN                                   CREATED
fra    node-playwright-firefox-q3m9k  running  <my-org>/node-playwright-firefox        4096MiB  1      bright-lake-dh6xp2sq.fra.unikraft.app  2 minutes ago
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
