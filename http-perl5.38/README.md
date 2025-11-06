# Perl

This guide explains how to create and deploy a simple Perl-based HTTP web server.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-perl5.38/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-perl5.38/
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
kraft cloud deploy -p 443:8080 -M 512 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: http-perl538-1p4ml
 ├────────── uuid: eabb0080-0065-40ff-81a8-f790f1b218ee
 ├───────── state: running
 ├─────────── url: https://cold-brook-ba71jc16.fra.unikraft.app
 ├───────── image: http-perl538@sha256:8c2c1f536b349c24e04ab4fec508b69f7f2349302d42a02855318ee55c12e37c
 ├───── boot time: 64.56 ms
 ├──────── memory: 512 MiB
 ├─────── service: cold-brook-ba71jc16
 ├── private fqdn: http-perl538-1p4ml.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/perl /usr/src/server.pl
```

In this case, the instance name is `http-perl538-1p4ml` and the address is `https://cold-brook-ba71jc16.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Perl-based HTTP web server:

```bash
curl https://cold-brook-ba71jc16.fra.unikraft.app
```
```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME                FQDN                                  STATE    STATUS          IMAGE                                  MEMORY   VCPUS  ARGS                              BOOT TIME
http-perl538-1p4ml  cold-brook-ba71jc16.fra.unikraft.app  running  37 seconds ago  http-perl538@sha256:8c2c1f536b349c...  512 MiB  1      /usr/bin/perl /usr/src/server.pl  64556us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-perl538-1p4ml
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.pl`: the actual Perl HTTP server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `server.pl` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
