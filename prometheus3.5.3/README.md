# Prometheus

This guide explains how to deploy [Prometheus](https://prometheus.io/) on Unikraft Cloud.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/prometheus3.5.3/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/prometheus3.5.3/
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

or

```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

Prometheus requires a volume to persist metrics data across restarts.
Create one before deploying:

```bash title="unikraft"
unikraft volume create --size 1Gi --metro fra prometheus-data
```

or

```bash title="kraft"
kraft cloud volume create --size 1Gi prometheus-data
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/prometheus353:latest
unikraft run --metro fra -p 443:9090/tls+http -m 1G --image <my-org>/prometheus353:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:9090 -M 1Gi .
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         prometheus-ivc2n
uuid:         0ea0e08e-a409-4d51-a529-b5e22763448a
state:        starting
image:        <my-org>/prometheus
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       summer-star-r568eklg
  name:       summer-star-r568eklg
  domains:
  - fqdn:     summer-star-r568eklg.fra.unikraft.app
networks:
- private-ip: 10.0.9.245
timestamps:
  created:    just now
```

or

```ansi title="kraft"
[●] Deployed successfully!
 │
 ├─────── name: prometheus-ivc2n
 ├─────── uuid: 0ea0e08e-a409-4d51-a529-b5e22763448a
 ├────── metro: fra
 ├────── state: starting
 ├───── domain: https://summer-star-r568eklg.fra.unikraft.app
 ├────── image: <my-org>/prometheus@sha256:
 ├───── memory: 1024 MiB
 ├──── service: summer-star-r568eklg
 └─ private ip: 10.0.9.245
```

In this case, the instance name is `prometheus-ivc2n` and the address is `https://summer-star-r568eklg.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the metrics endpoint of the Unikraft Cloud instance:

```bash
curl https://summer-star-r568eklg.fra.unikraft.app/metrics
```

```text
# TYPE go_gc_cycles_automatic_gc_cycles_total counter
go_gc_cycles_automatic_gc_cycles_total 5
# HELP go_gc_cycles_forced_gc_cycles_total Count of completed GC cycles forced by the application. Sourced from /gc/cycles/forced:gc-cycles.
# TYPE go_gc_cycles_forced_gc_cycles_total counter
go_gc_cycles_forced_gc_cycles_total 0
# HELP go_gc_cycles_total_gc_cycles_total Count of all completed GC cycles. Sourced from /gc/cycles/total:gc-cycles.
# TYPE go_gc_cycles_total_gc_cycles_total counter
go_gc_cycles_total_gc_cycles_total 5
# HELP go_gc_duration_seconds A summary of the wall-time pause (stop-the-world) duration in garbage collection cycles.
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

or

```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME              FQDN                                     STATE    STATUS        IMAGE                                              MEMORY    VCPUS  ARGS  BOOT TIME
prometheus-ivc2n  summer-star-r568eklg.fra.unikraft.app   running  1 minute ago  oci://unikraft.io/<my-org>/prometheus@sha256:...   1024 MiB  1            133.04 ms
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances remove prometheus-ivc2n
```

or

```bash title="kraft"
kraft cloud instance remove prometheus-ivc2n
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `prometheus.yml`: the Prometheus configuration file

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.

* `cmd: ["/bin/prometheus", ...]`: Use `/bin/prometheus` as the starting command of the instance, along with configuration flags.

Lines in the `Dockerfile` have the following roles:

* `FROM alpine:3.19 AS build`: Use Alpine Linux as the build stage to download the Prometheus release tarball.

* `RUN curl -fsSL ...`: Download and extract the Prometheus binary from the official GitHub release.

* `FROM alpine:3.19`: Use Alpine Linux as the final image to provide the required C libraries.

* `COPY --from=build /tmp/prometheus-release/prometheus /bin/prometheus`: Copy only the Prometheus binary into the final image.

* `COPY prometheus.yml /etc/prometheus/prometheus.yml`: Copy the Prometheus configuration file into the image.

The following options are available for customizing the app:

* Update `prometheus.yml` to change scrape targets, intervals, alerting rules, or any other Prometheus configuration.

* To persist metrics data across restarts, attach a volume and set `--storage.tsdb.path` to the volume mount path in the `cmd` section of the `Kraftfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

or

```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).