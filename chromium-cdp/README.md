# Chromium CDP

This example uses Chromium, a headless browser exposing a [CDP (Chrome DevTools Protocol)](https://chromedevtools.github.io/devtools-protocol/) websocket interface.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/chromium-cdp/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/chromium-cdp/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/chromium-cdp
unikraft run --metro fra \
  -m 4G \
  -p 443:8080/tls+http \
  --image <my-org>/chromium-cdp
```

The output shows the instance address and other details.

```ansi title="unikraft"
metro:        fra
name:         chromium-cdp-d0l6y
uuid:         debe81b0-8418-4e01-b795-b3546e0e5aac
state:        starting
image:        <my-org>/chromium-cdp
resources:
  memory:     4GiB
  vcpus:      1
service:
  uuid:       516e239b-2ab1-9fb9-599d-fb891cc39edb
  name:       spring-dream-p5wxwwl0
  domains:
  - fqdn:     spring-dream-p5wxwwl0.fra.unikraft.app
networks:
- uuid:       7d3633e4-7835-942c-7b32-5d392ba538d7
  private-ip: 10.0.4.141
  mac:        12:b0:7b:d3:eb:de
timestamps:
  created:    just now
```

In this case, the instance name is `chromium-cdp-d0l6y` and the address is `https://spring-dream-p5wxwwl0.fra.unikraft.app`.
They're different for each run.

To query the service you need to use a CDP client.
You can use the Python-based implementation in the `test/` directory.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                STATE    IMAGE                  ARGS  MEMORY   VCPUS  FQDN                                    CREATED
fra    chromium-cdp-d0l6y  running  <my-org>/chromium-cdp        4096MiB  1      spring-dream-p5wxwwl0.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete chromium-cdp-d0l6y
```

## Learn more

- [CDP Documentation](https://chromedevtools.github.io/devtools-protocol/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)


Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
