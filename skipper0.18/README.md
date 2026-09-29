# Skipper

This example uses [`Skipper`](https://opensource.zalando.com/skipper/), an HTTP router and reverse proxy for service composition

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/skipper0.18/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/skipper0.18/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/skipper018:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:9090/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/skipper018:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         skipper018-mx4ai
uuid:         34e3d740-c2b0-4644-b7e1-647350f688dc
state:        starting
image:        <my-org>/skipper018
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       b32c9035-d669-79fa-9955-9ad52cd1fcb4
  name:       aged-sea-o7d3c42s
  domains:
  - fqdn:     aged-sea-o7d3c42s.fra.unikraft.app
networks:
- uuid:       70cfb329-9ab3-fc8c-aff9-a3bbbbeb70f3
  private-ip: 10.0.6.4
  mac:        12:b0:32:1b:02:7b
timestamps:
  created:    just now
```

In this case, the instance name is `skipper018-mx4ai` and the address is `https://aged-sea-o7d3c42s.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Skipper.

```bash
curl https://aged-sea-o7d3c42s.fra.unikraft.app
```

```text
Hello, world from Skipper on Unikraft!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME              STATE    IMAGE                ARGS  MEMORY  VCPUS  FQDN                                CREATED
fra    skipper018-mx4ai  running  <my-org>/skipper018        256MiB  1      aged-sea-o7d3c42s.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete skipper018-mx4ai
```

## Customize your app

To customize Skipper you can change the `example.eskip` configuration file.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
