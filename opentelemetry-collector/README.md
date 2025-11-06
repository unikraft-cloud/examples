# OpenTelemetry Collector

This example uses [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/), a vendor-agnostic
implementation of how to receive, process and export telemetry data.
OpenTelemetry Collector works with Unikraft / Unikraft Cloud to process telemetry data.

To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/opentelemetry-collector/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/opentelemetry-collector/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash
kraft cloud deploy -M 1024M .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: opentelemetry-collector-bvtnh
 ├────────── uuid: 40e8b154-b3b6-4312-ae69-2cdb794b15e4
 ├───────── state: starting
 ├───────── image: opentelemetry-collector@sha256:64f73ea5fe208f54e5212f57979f24bebcf36276495462c52b380d15dd539ced
 ├──────── memory: 976 MiB
 ├── private fqdn: opentelemetry-collector-bvtnh.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/otelcontribcol --config /etc/otel/config.yaml
```

In this case, the instance name is `opentelemetry-collector-bvtnh`.
They're different for each run.

Note that the instance doesn't export a service.
The default configuration can receive telemetry data from other instances by specifying the private IP or internal DNS as destination.
The only configured exporter is the debug exporter.
Feel free to change and redeploy!

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME                           FQDN  STATE    STATUS        IMAGE             MEMORY   VCPUS  ARGS                                 BOOT TIME
opentelemetry-collector-bvtnh        running  since 11mins  opentelemetry...  976 MiB  1      /usr/bin/otelcontribcol --config...  177.62 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove opentelemetry-collector-bvtnh
```

## Customize your app

To customize the OpenTelemetry Collector app, update `Kraftfile` or, more likely, the `rootfs/etc/otel/config.yaml` files:

You can update the `rootfs/etc/otel/config.yaml` file as detailed in the [documentation](https://opentelemetry.io/docs/collector/configuration/).
Such as adding another export, apart from the debug exporter.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
