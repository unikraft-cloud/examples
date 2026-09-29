# Prometheus and Grafana

[Prometheus](https://prometheus.io) is a monitoring system and time-series database, and [Grafana](https://grafana.com) is an open source analytics and visualization platform.
This example deploys both on Unikraft Cloud to chart the [instance metrics](https://unikraft.com/docs/platform/metrics) of your own account: Prometheus scrapes the metrics endpoint over a private network, and Grafana serves a pre-built dashboard behind a public port.

The dashboard is a starting point rather than a supported product surface.
Rename panels, drop rows you don't need, and tune the alert thresholds to your workload.

## Deployment

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/prometheus-grafana` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/prometheus-grafana/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

## Configure

The configuration files ship to each instance as read-only [ROMs](https://unikraft.com/docs/features/roms), uploaded when the instance starts.
Finish this section **before** deploying: changing a file later means deploying again with a new ROM, not editing a file in place.

Fill in your metro and API token in [`prometheus/rom/prometheus.yml`](./prometheus/rom/prometheus.yml):

```bash
export UKC_TOKEN=<token>
sed -i "s/<metro>/fra/g; s/<UKC_TOKEN>/${UKC_TOKEN}/" prometheus/rom/prometheus.yml
```

> **Warning**:
> A Unikraft Cloud API token is not read-only.
> The same token that reads metrics can also create, stop, and **delete** instances and volumes in your account.
> Never commit `prometheus.yml` with a real token filled in, and rotate the token if it lands somewhere unexpected.

The repository ships these files:

| File | Purpose |
| ---- | ------- |
| `prometheus/rom/prometheus.yml` | Scrape config for `/v1/instances/metrics`. Mounted at `/etc/prometheus`. |
| `prometheus/rom/alerts.yml` | Five starter alerting rules. |
| `grafana/provisioning/datasources/datasource.yml` | Points Grafana at the Prometheus instance. Mounted at `/etc/grafana/provisioning`. |
| `grafana/provisioning/dashboards/dashboards.yml` | Loads dashboards from the ROM directory. |
| `grafana/dashboards/vm-instances.json` | The VM instances dashboard. Mounted at `/var/lib/grafana/dashboards`. |

## Prometheus

Create a volume so the time-series database survives a restart:

```bash title="unikraft"
unikraft volume create --metro fra --name prometheus-data --size 1G
```

```ansi title="unikraft"
metro:        fra
name:         prometheus-data
uuid:         689b21aa-8f2c-4d94-ba84-947119c11bc9
state:        available
size:         1GiB
filesystem:   ext4
quota-policy: static
persistent:   true
access-mode:  rwo
timestamps:
  created:    just now
```

Build and deploy Prometheus.
It gets an internal domain and no published port, so only Grafana on the same private network can reach it:

```bash title="unikraft"
unikraft build prometheus/ --output <my-org>/prometheus:latest

unikraft run --metro fra \
  --name prometheus \
  -m 1024M \
  --domain prometheus-internal.internal. \
  --rom dir=./prometheus/rom,at=/etc/prometheus \
  --volume prometheus-data:/prometheus \
  --image <my-org>/prometheus:latest
```

The output shows the instance details:

```ansi title="unikraft"
metro:        fra
name:         prometheus
uuid:         7b71c6ec-1029-4040-b134-1eec95421f0b
state:        starting
image:        <my-org>/prometheus
resources:
  memory:     1GiB
  vcpus:      1
service:
  name:       rough-river-122ff7v6
  uuid:       ccc672b5-adda-4150-a5b7-1f438467d87d
  domains:
  - fqdn:     prometheus-internal.internal
volumes:
- name:       prometheus-data
  uuid:       689b21aa-8f2c-4d94-ba84-947119c11bc9
  at:         /prometheus
roms:
- name:       etc-prometheus
  image:      7e85d7d4-4d33-411c-9560-36978707202e
  at:         /etc/prometheus
networks:
- uuid:       08305497-be6b-4786-801a-70f4aad8ad2a
  private-ip: 10.0.0.65
  mac:        12:b0:0a:00:00:41
timestamps:
  created:    just now
```

The `domains` entry confirms the internal FQDN, and the `roms` entry confirms the config directory was uploaded and mounted.

> **Warning**:
> Don't publish a port for Prometheus.
> It has no authentication of its own, so exposing it would hand your metrics, and the alert rules describing your estate, to anyone who finds the address.

> **Note**:
> Don't enable scale-to-zero on Prometheus either.
> A sleeping Prometheus stops scraping, which leaves gaps in the data.

## Grafana

Build and deploy Grafana, this time with a public port:

```bash title="unikraft"
unikraft build grafana/ --output <my-org>/grafana:latest

unikraft run --metro fra \
  --name grafana \
  -p 443:3000/tls+http \
  -m 1024M \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  -e GF_SECURITY_ADMIN_USER=admin \
  -e GF_SECURITY_ADMIN_PASSWORD=<password> \
  -e GF_USERS_ALLOW_SIGN_UP=false \
  -e GF_ANALYTICS_REPORTING_ENABLED=false \
  -e GF_ANALYTICS_CHECK_FOR_UPDATES=false \
  --rom dir=./grafana/provisioning,at=/etc/grafana/provisioning \
  --rom dir=./grafana/dashboards,at=/var/lib/grafana/dashboards \
  --image <my-org>/grafana:latest
```

> **Warning**:
> Port 443 makes Grafana reachable by anyone who knows its address, with only the login in front of your metrics.
> Choose a strong, unique `<password>` rather than the placeholder, and keep `GF_USERS_ALLOW_SIGN_UP=false` so visitors can't create their own accounts.

The output shows the generated address under `domains`:

```ansi title="unikraft"
metro:                              fra
name:                               grafana
uuid:                               43e60d11-3db3-4da2-a491-5abd869eae3e
state:                              starting
image:                              <my-org>/grafana
runtime:
  env:
    GF_ANALYTICS_CHECK_FOR_UPDATES: false
    GF_ANALYTICS_REPORTING_ENABLED: false
    GF_SECURITY_ADMIN_PASSWORD:     *
    GF_SECURITY_ADMIN_USER:         admin
    GF_USERS_ALLOW_SIGN_UP:         false
resources:
  memory:                           1GiB
  vcpus:                            1
service:
  name:                             twilight-brook-c7ps65ek
  uuid:                             3e220713-e378-441c-80e5-25ace1474714
  domains:
  - fqdn:                           twilight-brook-c7ps65ek.fra.unikraft.app
roms:
- name:                             etc-grafana-provisioning
  image:                            0f6ea33c-e602-4932-acf0-3c7a14cdca97
  at:                               /etc/grafana/provisioning
- name:                             var-lib-grafana-dashboards
  image:                            2a479b52-0d6f-4a93-a930-1a19de9bec8c
  at:                               /var/lib/grafana/dashboards
networks:
- uuid:                             96ebdef3-7a98-46c0-9b7b-5c8ebb310620
  private-ip:                       10.0.0.49
  mac:                              12:b0:0a:00:00:31
timestamps:
  created:                          just now
scale-to-zero:
  enabled:                          true
  policy:                           on
  stateful:                         true
  cooldown-time:                    1s
```

The FQDN is generated for you, and it differs on each run.
The CLI masks `GF_SECURITY_ADMIN_PASSWORD` in its output, but the value still reaches the instance as an environment variable.

Point your browser at the address and log in with the credentials you set above.
The dashboard appears in the **Unikraft Cloud** folder.

Data appears after the first couple of scrapes.
The `rate()`-based panels need one to two minutes of history before they render anything.

You can list information about the instances by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME        STATE    IMAGE                ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    grafana     standby  <my-org>/grafana           1GiB    1      twilight-brook-c7ps65ek.fra.unikraft.app  just now
fra    prometheus  running  <my-org>/prometheus        1GiB    1      prometheus-internal.internal              6 minutes ago
```

Grafana shows as `standby` rather than `running` because `cooldown-time=1000` is 1000 **milliseconds**, so it parks almost immediately when idle.
The next request wakes it.

When done, you can remove the instances and the volume:

```bash title="unikraft"
unikraft instances delete grafana prometheus
unikraft volume delete prometheus-data
```

## What the dashboard shows

The dashboard holds 24 panels across five rows, driven by the metrics that the [instance metrics reference](https://unikraft.com/docs/platform/metrics) documents:

| Row | Panels |
| --- | ------ |
| Fleet overview | Instance counts by state, total resident memory, active connections, and a per-instance state table |
| Resource usage | CPU time rate in cores, resident memory, uptime, and restarts per hour |
| Network | Inbound and outbound throughput, plus packet rates |
| Requests and connections | Active, queued, and processed connections or requests |
| Boot and wakeup latency | Boot, network setup, and template creation times, with wakeup latency percentiles and a heatmap |

A **Data source** variable selects which Prometheus to query, and an **Instance** variable filters by `instance_uuid`.

## What to watch out for

A few behaviours surprise people the first time:

- **The endpoint reports only live instances.**
  An instance appears only while a live virtual machine backs it, so a fully stopped instance produces no series at all.
  Don't build a "stopped instances" count on this endpoint, because it would always read zero.

- **Per-instance identity lives in `instance_uuid`.**
  Prometheus injects its own `instance` label holding the API host it scraped, which is identical for every instance.
  Group and join on `instance_uuid` instead.

- **Panels label each series by UUID.**
  The Prometheus exposition carries no instance name, so legends show raw UUIDs.

- **Counters restart from zero.**
  CPU time, the byte and packet counters, and the processed-request counter are reported since the last start of the instance, so a restart resets them.
  The `rate()`-based panels handle the reset.

- **The wakeup latency panels stay empty without scale-to-zero.**
  Only instances with [scale-to-zero](https://unikraft.com/docs/features/scale-to-zero) enabled record the histogram.

## Customize your app

To customize the app, update the files in the repository, listed below:

* `prometheus/rom/prometheus.yml`: scrape targets, intervals, and labels.
  To watch more than one metro, add a `static_configs` entry per metro, each with its own `region` label.
* `prometheus/rom/alerts.yml`: alerting rules and thresholds.
* `grafana/provisioning/`: the Grafana data source and dashboard provider.
* `grafana/dashboards/vm-instances.json`: the dashboard itself.
* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

The dashboard queries carry a hard-coded `job="instances"` selector.
If you rename the job in `prometheus.yml`, update the dashboard queries to match, or every panel reads "No data".

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
