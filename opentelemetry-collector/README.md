# OpenTelemetry Collector on KraftCloud

The [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) offers a vendor-agnostic implementation of how to receive, process and export telemetry data.


To run OpenTelemetry Collector on KraftCloud, clone this examples repository and `cd` into this directory, then invoke:

```console
kraft cloud deploy .
```

The command will build and deploy the files under `rootfs` in a Collector instance. The default configuration can receive telemetry data from other instances by specifying the private IP or internal DNS as destination. The only configured exporter is the debug exporter. Feel free to modify and redeploy!

If you want to use your own configuration, please note that you have to disable the self-telemetry feature:

```yaml
service:
  telemetry:
    metrics:
      level: none
```

## Learn more

- [OpenTelemetry Collectors Documentation](https://opentelemetry.io/docs/collector/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)

