# MariaDB

This guide shows you how to use [MariaDB](https://mariadb.org), one of the most popular open source relational databases.
To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/mariadb/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/mariadb
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/mariadb:latest
unikraft run --metro fra \
  -m 1G \
  -p 3306:3306/tls \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  -e MARIADB_ROOT_PASSWORD="unikraft" \
  --image <my-org>/mariadb:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         mariadb-w2g2z
uuid:         ba696c22-adff-4fba-88b9-d1b790ca2357
state:        starting
image:        <my-org>/mariadb
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       ca8ae7e9-3767-85f6-3d70-b77bcf894a7c
  name:       twilight-sun-82lt4ddk
  domains:
  - fqdn:     twilight-sun-82lt4ddk.fra.unikraft.app
networks:
- uuid:       935ba4ef-39c2-07e7-d2ae-8cd3c9aae07c
  private-ip: 10.0.6.3
  mac:        12:b0:ee:29:71:e4
timestamps:
  created:    just now
```

In this case, the instance name is `mariadb-w2g2z` which is different for each run.

To test the deployment, first forward the port with the `socat` command.

```bash
socat TCP-LISTEN:3306,reuseaddr,fork OPENSSL:twilight-sun-82lt4ddk.fra.unikraft.app:3306,verify=0
```

You can now, on a separate console, use the `mysql` command line tool to test that the set up works:

```bash
mysql -h 127.0.0.1 --ssl-mode=DISABLED -u root -punikraft mysql <<< "select count(*) from user"
```

Or use the `mariadb` client command line tool:

```bash
mariadb -h 127.0.0.1 --ssl=OFF -u root -punikraft mysql <<< "select count(*) from user"
```

You should see output such as:

```ansi
count(*)
6
```

To disconnect, kill the `socat` command using `Ctrl+c`.

> **Note:**
> This guide uses `socat` for port forwarding only when a service doesn't support TLS and isn't HTTP-based (TLS/SNI determines the correct instance to send traffic to).
> Also note that port forwarding isn't needed when connecting via an instance's private IP/FQDN.
> For example, when a MariaDB instance serves as a database server to
> another instance that acts as a frontend and which **does** support TLS.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME           STATE    IMAGE             ARGS  MEMORY   VCPUS  FQDN                                    CREATED
fra    mariadb-w2g2z  running  <my-org>/mariadb        1024MiB  1      twilight-sun-82lt4ddk.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instance remove mariadb-w2g2z
```

> **Tip:**
> This example uses the [`idle` scale-to-zero policy](https://unikraft.com/docs/api/platform/v1/instances#scaletozero_policy) by default (see the `labels` section in the `Kraftfile`).

## Using volumes

You can use [volumes](https://unikraft.com/docs/platform/volumes) for data persistence for your MariaDB instance.
For that you would first create a volume:

```bash title="unikraft"
unikraft volume create --set metro=fra --set name=mariadb-store --set size=512M
```

Then start the MariaDB instance and mount that volume:

```bash title="unikraft"
unikraft build . --output <my-org>/mariadb:latest
unikraft run --metro fra \
  -m 1G \
  -p 3306:3306/tls \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  -e MARIADB_ROOT_PASSWORD="unikraft" \
  --volume mariadb-store:/var/lib \
  --image <my-org>/mariadb:latest
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
