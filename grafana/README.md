# Grafana

This guide shows you how to use [Grafana](https://grafana.com), the open source analytics & monitoring solution for every database.

To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/grafana/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/grafana/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/grafana:latest
unikraft run --metro fra \
  -m 2G \
  -p 443:3000/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/grafana:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         grafana-sikrv
uuid:         1d8f0b36-39ff-45a2-8baa-664640c60885
state:        starting
image:        <my-org>/grafana
resources:
  memory:     2048MiB
  vcpus:      1
service:
  uuid:       baedae7b-0836-4b53-d1f5-a6bbcd373155
  name:       dawn-water-4jlnvgpy
  domains:
  - fqdn:     dawn-water-4jlnvgpy.fra.unikraft.app
networks:
- uuid:       de0faba6-9c16-f108-a32a-f6bc4133a9cd
  private-ip: 10.0.6.6
  mac:        12:b0:fb:95:5b:66
timestamps:
  created:    just now
```

In this case, the instance name is `grafana-sikrv` and the address is `https://icy-sea-i6m5fwyk.fra.unikraft.app`.
They're different for each run.

To test, point your browser at the address.
The default account/password are `admin/admin` (the system will prompt you to change the password).

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME           STATE    IMAGE             ARGS  MEMORY   VCPUS  FQDN                               CREATED
fra    grafana-sikrv  running  <my-org>/grafana        2048MiB  1      icy-sea-i6m5fwyk.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete grafana-sikrv
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

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
