# OpenTelemetry Collector

This example uses [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/), a vendor-agnostic
implementation of how to receive, process and export telemetry data.
OpenTelemetry Collector works with Unikraft / Unikraft Cloud to process telemetry data.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/opentelemetry-collector/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/opentelemetry-collector/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/opentelemetry-collector:latest
unikraft run --metro fra \
  -m 1536M \
  --image <my-org>/opentelemetry-collector:latest
```

The output shows the instance details:

```ansi title="unikraft"
metro:        fra
name:         opentelemetry-collector-bvtnh
uuid:         40e8b154-b3b6-4312-ae69-2cdb794b15e4
state:        starting
image:        <my-org>/opentelemetry-collector
resources:
  memory:     1536MiB
  vcpus:      1
networks:
- uuid:       e74ba590-cbec-404b-d076-16aca1b52404
  private-ip: 10.0.3.3
  mac:        12:b0:aa:f7:b9:26
timestamps:
  created:    just now
```

In this case, the instance name is `opentelemetry-collector-bvtnh`.
They're different for each run.

Note that the instance doesn't export a service.
The default configuration can receive telemetry data from other instances by specifying the private IP or internal DNS as destination.
Use port 4317 for gRPC and port 4318 for HTTP.
The only configured exporter is the debug exporter.
Feel free to change and redeploy!

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                           STATE    IMAGE                   ARGS  MEMORY   VCPUS  FQDN  CREATED
fra    opentelemetry-collector-bvtnh  running  <my-org>/opentelemetry        1536MiB  1            2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete opentelemetry-collector-bvtnh
```

## Customize your app

To customize the OpenTelemetry Collector app, update `Kraftfile` or, more likely, the `rootfs/etc/otel/config.yaml` files:

You can update the `rootfs/etc/otel/config.yaml` file as detailed in the [documentation](https://opentelemetry.io/docs/collector/configuration/).
Such as adding another export, apart from the debug exporter.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
