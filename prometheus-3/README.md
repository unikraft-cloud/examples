# Prometheus3

This guide shows you how to use [Prometheus](https://prometheus.io/), an open source systems monitoring and alerting toolkit.

To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/prometheus/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/prometheus/
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

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/prometheus:latest
unikraft run --metro fra -p 443:9090/tls+http -m 2G --image <my-org>/prometheus:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:9090 -M 2Gi .
```

The output shows the instance address and other details:

```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: prometheus-xk7pq
 ├───────── uuid: 7f3a2c91-df14-4b08-ae31-c2e085f30a11
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://bright-rain-7xk2mn4p.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/prometheus@sha256:9bcd3451aa72b4ef8a8c1f20302bb84f1570443a93ab9698c1f1e02602bb1234
 ├─────── memory: 2048 MiB
 ├────── service: bright-rain-7xk2mn4p
 ├─ private fqdn: prometheus-xk7pq.internal
 └─── private ip: 10.0.3.1
```

or

```ansi title="unikraft"
metro:        fra
name:         prometheus-xk7pq
uuid:         7f3a2c91-df14-4b08-ae31-c2e085f30a11
state:        starting
image:        <my-org>/prometheus
resources:
  memory:     2048MiB
  vcpus:      1
service:
  uuid:       12bc9041-c23d-4f8a-bb12-8acde3512f7c
  name:       bright-rain-7xk2mn4p
  domains:
  - fqdn:     bright-rain-7xk2mn4p.fra.unikraft.app
networks:
- uuid:       a3ccf7b2-82e4-6693-14b3-2f53663g5eae
  private-ip: 10.0.3.1
  mac:        12:b0:c0:f1:06:cd
timestamps:
  created:    just now
```

In this case, the instance name is `prometheus-xk7pq` and the address is `https://bright-rain-7xk2mn4p.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Prometheus metrics endpoint on the Unikraft Cloud instance:

```bash
curl https://bright-rain-7xk2mn4p.fra.unikraft.app/metrics
```

You can also open the Prometheus web UI in your browser:

```
https://bright-rain-7xk2mn4p.fra.unikraft.app
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME              STATE    IMAGE                ARGS  MEMORY  VCPUS  FQDN                                   CREATED
fra    prometheus-xk7pq  running  <my-org>/prometheus        2.0GiB  1      bright-rain-7xk2mn4p.fra.unikraft.app  2 minutes ago
```

or

```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME              FQDN                                   STATE    STATUS         IMAGE                                             MEMORY   VCPUS  ARGS  BOOT TIME
prometheus-xk7pq  bright-rain-7xk2mn4p.fra.unikraft.app  running  2 minutes ago  oci://unikraft.io/<my-org>/prometheus@sha256:...  2.0 GiB  1            412.53 ms
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete prometheus-xk7pq
```

or

```bash title="kraft"
kraft cloud instance remove prometheus-xk7pq
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `prometheus.yml`: the Prometheus configuration file
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Dockerfile` have the following roles:

* `FROM alpine:latest`: Use the latest Alpine Linux image as the base. 
  *(Note: The directory for this example is explicitly named `prometheus-3` because `alpine:latest` currently provides the 3.x series of Prometheus. This version pinning ensures the `prometheus.yml` configuration remains compatible and future-proofs the example against breaking changes in future major releases).*

* `RUN apk add --no-cache prometheus`: Install Prometheus via the Alpine package manager.

* `EXPOSE 9090`: Expose port `9090`, the default Prometheus HTTP port.

* `ENTRYPOINT ["/usr/bin/prometheus", ...]`: Start Prometheus with the provided configuration file and storage path.

Key sections in `prometheus.yml` have the following roles:

* `global`: Sets global defaults for `scrape_interval`, `scrape_timeout`, and `evaluation_interval`, as well as `external_labels` attached to all time series and alerts.

* `rule_files`: Specifies paths to alerting and recording rule files to load.

* `alerting`: Configures the Alertmanager instances Prometheus should send alerts to.

* `scrape_configs`: Defines the targets Prometheus scrapes for metrics. The default configuration includes:
  - `prometheus`: Prometheus scrapes itself at `localhost:9090`.
  - `node`: Scrapes a Node Exporter instance at `node-exporter:9100` for host-level metrics.
  - `my-app`: An example job showing how to scrape a custom application.

The following options are available for customizing the app:

* To add or remove scrape targets, edit the `scrape_configs` section in `prometheus.yml`.

* To adjust how frequently metrics are collected, change the `scrape_interval` and `evaluation_interval` values under `global`.

* To load alerting or recording rules, place rule files under a `rules/` directory and reference them in the `rule_files` section.

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
