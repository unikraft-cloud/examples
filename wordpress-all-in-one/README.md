# Wordpress

This guide shows you how to use [Wordpress](https://wordpress.com/), a web content management system.

To run it, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/wordpress-all-in-one/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/wordpress-all-in-one/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

> **Note:**
> A Wordpress instance on Unikraft Cloud requires 3GB to run.
> Request an increase in the instance memory quota when you need more memory.

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash
kraft cloud deploy -p 443:3000 -M 3072 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: wordpress-fx5rb
 ├────────── uuid: bfb9d151-1604-452a-b2e0-f737486744df
 ├───────── state: starting
 ├──────── domain: https://cool-silence-h5c1es4z.fra.unikraft.app
 ├───────── image: wordpress@sha256:3e116e6c74dd04e19d4062a14f8173974ba625179ace3c10a2c96546638c4cd8
 ├──────── memory: 3072 MiB
 ├─────── service: cool-silence-h5c1es4z
 ├── private fqdn: wordpress-fx5rb.internal
 ├──── private ip: 172.16.3.1
 └────────── args: /usr/local/bin/wrapper.sh
```

In this case, the instance name is `wordpress-fx5rb`.
They're different for each run.

Use a browser to access the install page of Wordpress.
Fill out the form and complete the Wordpress install.

You can list information about the instance by running:

```bash
kraft cloud inst list
```

```ansi
NAME             FQDN                                    STATE    STATUS       IMAGE                 MEMORY   VCPUS  ARGS                       BOOT TIME
wordpress-fx5rb  cool-silence-h5c1es4z.fra.unikraft.app  running  since 2mins  wordpress@sha256:...  3.0 GiB  1      /usr/local/bin/wrapper.sh  1708.17 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove wordpress-fx5rb
```

## Customize your deployment

The current deployment uses the current stable version of Wordpress (6.5.5).
It also uses hard-coded values for the database name, user name, passwords.
You can update the `Dockerfile` with other names.
Or expand the configuration to feature non-hard-coded values.

You can deploy WordPress modules in the WordPress instance without affecting the build.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
