# Grafana

This guide shows you how to use [Grafana](https://grafana.com), the open source analytics & monitoring solution for every database.

To run it, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/grafana/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/grafana/
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
kraft cloud deploy -p 443:3000 -M 1024 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: grafana-sikrv
 ├────────── uuid: 1d8f0b36-39ff-45a2-8baa-664640c60885
 ├───────── state: running
 ├─────────── url: https://icy-sea-i6m5fwyk.fra.unikraft.app
 ├───────── image: grafana@sha256:484d6f98cdc321443188b8f2900035182dffdb45069f3cd087dcb6851ddff3bc
 ├───── boot time: 502.65 ms
 ├──────── memory: 1024 MiB
 ├─────── service: dawn-water-4jlnvgpy
 ├── private fqdn: grafana-mgby4.internal
 ├──── private ip: 172.16.6.6
 └────────── args: /usr/share/grafana/bin/grafana server -homepath /usr/share/grafana/
```

In this case, the instance name is `grafana-sikrv` and the address is `https://icy-sea-i6m5fwyk.fra.unikraft.app`.
They're different for each run.

To test, point your browser at the address.
The default account/password are `admin/admin` (the system will prompt you to change the password).

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME           FQDN                               STATE    STATUS          IMAGE                        MEMORY    VCPUS  ARGS                                      BOOT TIME
grafana-sikrv  icy-sea-i6m5fwyk.fra.unikraft.app  running  11 minutes ago  grafana@sha256:484d6f98c...  1024 MiB  1      /usr/share/grafana/bin/grafana server...  502651us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove grafana-sikrv
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

The following options are available for customizing the app:

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.
  See the commented out `COPY` command in the `Dockerfile`.

* If you use a new executable, update the `cmd` line in the `Kraftfile` and replace `/usr/share/grafana/bin/grafana` with the path to the new executable.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
