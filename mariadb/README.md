# MariaDB

This guide shows you how to use [MariaDB](https://mariadb.org), one of the most popular open source relational databases.
To run it, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/mariadb/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/mariadb
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
kraft cloud deploy -p 3306:3306/tls -M 1024 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: mariadb-w2g2z
 ├────────── uuid: ba696c22-adff-4fba-88b9-d1b790ca2357
 ├───────── state: running
 ├────────── fqdn: twilight-sun-82lt4ddk.fra.unikraft.app
 ├───────── image: mariadb@sha256:6e31d28b351eb12a070e3074f0a500532d0a494332947e9d8dbfa093d2d551fd
 ├───── boot time: 159.06 ms
 ├──────── memory: 1024 MiB
 ├─────── service: twilight-sun-82lt4ddk
 ├── private fqdn: mariadb-w2g2z.internal
 ├──── private ip: 172.16.6.3
 └────────── args: /usr/sbin/mariadbd --user=root --log-bin
```

In this case, the instance name is `mariadb-w2g2z` which is different for each run.

To test the deployment, first forward the port with the `kraft cloud tunnel` command.

```bash
kraft cloud tunnel 3306:mariadb-w2g2z:3306
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

To disconnect, kill the `tunnel` command using `Ctrl+c`.

> **Note:**
> This guide uses `kraft cloud tunnel` only when a service doesn't support TLS and isn't HTTP-based (TLS/SNI determines the correct instance to send traffic to).
> Also note that the `tunnel` command isn't needed when connecting via an instance's private IP/FQDN.
> For example when the MariaDB instance serves as a database server to another instance that acts as a frontend and which **does** support TLS.

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME           FQDN                                    STATE    STATUS        IMAGE         MEMORY   VCPUS  ARGS                             BOOT TIME
mariadb-w2g2z  twilight-sun-82lt4ddk.fra.unikraft.app  running  1 minute ago  mariadb@s...  1.0 GiB  1      /usr/sbin/mariadbd --user=ro...  159065us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove mariadb-w2g2z
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
