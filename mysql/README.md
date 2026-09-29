# MySQL

This guide shows you how to use [MySQL](https://www.mysql.com), one of the most popular open source relational databases.
To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/mysql/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/mysql
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/mysql:latest
unikraft run --metro fra \
  -m 1G \
  -p 3306:3306/tls \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  -e MYSQL_ROOT_PASSWORD="unikraft" \
  --image <my-org>/mysql:latest
```

The output shows the instance address and other details:

```ansi
metro:        fra
name:         mysql-b3mlh
uuid:         19479d80-0995-4ed2-b08e-86b29eda3f3
state:        starting
image:        <my-org>/mysql
runtime:
  env:
    MYSQL_ROOT_PASSWORD: *
resources:
  memory:                1GiB
  vcpus:                 1
service:
  name:                  purple-wood-hqb663gu
  uuid:                  d2bcd1c0-c980-4d5b-9777-2bec2b0d0645
  domains:
  - fqdn:                purple-wood-hqb663gu.fra.unikraft.app
networks:
- uuid:                  3e3a6cd5-ca66-41ec-8c28-5280b049f732
  private-ip:            10.0.14.181
  mac:                   12:b0:0a:00:0e:b5
timestamps:
  created:               just now
scale-to-zero:
  enabled:               true
  policy:                idle
  stateful:              true
  cooldown-time:         1s
```

In this case, the instance name is `mysql-b3mlh` which is different for each run.

To test the deployment, first forward the port with the `socat` command.

```bash
socat TCP-LISTEN:3306,reuseaddr,fork OPENSSL:purple-wood-hqb663gu.fra.unikraft.app:3306,verify=0
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
> For example, when a MySQL instance serves as a database server to another instance that acts as a frontend and which **does** support TLS.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME         STATE    IMAGE           ARGS  MEMORY   VCPUS  FQDN                                    CREATED
fra    mysql-b3mlh  running  <my-org>/mysql        1024MiB  1      purple-wood-hqb663gu.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instance remove mysql-b3mlh
```

> **Tip:**
> This example uses the [`idle` scale-to-zero policy](https://unikraft.com/docs/api/platform/v1/instances#scaletozero_policy) by default.

## Using volumes

You can use [volumes](https://unikraft.com/docs/platform/volumes) for data persistence for your MySQL instance.
For that you would first create a volume:

```bash title="unikraft"
unikraft volume create --set metro=fra --set name=mysql-store --set size=512M
```

Then start the MySQL instance and mount that volume:

```bash
unikraft build . --output <my-org>/mysql:latest
unikraft run --metro fra \
  -m 1G \
  -p 3306:3306/tls \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  -e MYSQL_ROOT_PASSWORD="unikraft" \
  --volume mysql-store:/var/lib \
  --image <my-org>/mysql:latest
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
