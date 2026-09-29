# C HTTP Server

This guide explains how to create and deploy a C app.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-gcc13.2` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-gcc13.2/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-gcc132:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-gcc132:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-gcc132-is2s9
uuid:         bec814ce-6ed5-4858-b247-e7f0b17750f5
state:        starting
image:        <my-org>/httpserver-gcc132
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       c36a4df6-b78d-677e-ea24-3e7a519a4130
  name:       still-resonance-bja3lste
  domains:
  - fqdn:     still-resonance-bja3lste.fra.unikraft.app
networks:
- uuid:       0f17e562-b57a-d40b-eecc-74e9058ecaaf
  private-ip: 10.0.0.49
  mac:        12:b0:10:70:49:2f
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-gcc132-is2s9` and the address is `https://still-resonance-bja3lste.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance:

```bash
curl https://still-resonance-bja3lste.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                     STATE    IMAGE                       ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    httpserver-gcc132-is2s9  standby  <my-org>/httpserver-gcc132        256MiB  1      still-resonance-bja3lste.fra.unikraft…  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-gcc132-is2s9
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
