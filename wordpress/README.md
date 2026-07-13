# Wordpress with Nginx and MariaDB

This guide explains how to create and deploy a Wordpress app with Nginx and MariaDB.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/wordpress` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/wordpress/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft login
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

## Create Volumes

Create the volumes for the Wordpress and MariaDB data:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume create --metro fra --name wordpress-wordpress-data --size 512M
unikraft volume create --metro fra --name wordpress-db-data --size 512M
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume create --name wordpress-wordpress-data --size 512Mi
kraft cloud volume create --name wordpress-db-data --size 512Mi
```

You can list the created volumes by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume list
```

```ansi title="unikraft"
METRO  NAME                      STATE      SIZE    CREATED
fra    wordpress-db-data         available  512MiB  just now
fra    wordpress-wordpress-data  available  512MiB  just now
```

or


**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume list
```

```ansi title="kraft"
NAME                      CREATED AT  SIZE     ATTACHED TO  MOUNTED BY  STATE      PERSISTENT
wordpress-wordpress-data  now         512 MiB                           available  true
wordpress-db-data         now         512 MiB                           available  true
```

## Deploy MariaDB

Build and deploy the MariaDB instance.
MariaDB is an internal service (not publicly accessible), reached via the `wordpress-mariadb.internal` domain by default.
If you choose a different internal domain, make sure to set `WORDPRESS_DB_HOST` to the same value when deploying WordPress.

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./mariadb --output <my-org>/mariadb:latest
unikraft run --name mariadb --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -m 1G --volume wordpress-db-data:/var/lib/mysql --image <my-org>/mariadb:latest --domain wordpress-mariadb.internal --env MARIADB_ROOT_PASSWORD=unikraft
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --name mariadb --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s -M 1Gi --volume wordpress-db-data:/var/lib/mysql --domain wordpress-mariadb.internal --env MARIADB_ROOT_PASSWORD=unikraft ./mariadb/
```

Make sure to replace `<my-org>` with your username / org-name.

The output shows the instance details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:                     fra
name:                      mariadb
uuid:                      3af0eefb-29a8-4634-9b94-abf62d2fb90a
state:                     starting
image:                     <my-org>/mariadb
runtime:
  env:
    MARIADB_ROOT_PASSWORD: *
resources:
  memory:                  1GiB
  vcpus:                   1
service:
  name:                    snowy-glitter-3uylzbqk
  uuid:                    0b3303d0-1a2e-4353-a9c7-29151263ef9f
  domains:
  - fqdn:                  wordpress-mariadb.internal
volumes:
- name:                    wordpress-db-data
  uuid:                    7b232d0f-dfbf-4ff7-9208-106b5d92bbe3
  at:                      /var/lib/mysql
networks:
- uuid:                    8cad0682-a700-4303-af8c-ebd18465ed32
  private-ip:              10.0.1.73
  mac:                     12:b0:0a:00:01:49
timestamps:
  created:                 just now
scale-to-zero:
  enabled:                 true
  policy:                  idle
  stateful:                true
  cooldown-time:           1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: mariadb
 ├───────── uuid: 3af0eefb-29a8-4634-9b94-abf62d2fb90a
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: wordpress-mariadb.internal
 ├──────── image: oci://unikraft.io/<my-org>/mariadb@sha256:cf1...
 ├─────── memory: 1024 MiB
 ├────── service: snowy-glitter-3uylzbqk
 ├─ private fqdn: mariadb.internal
 └─── private ip: 10.0.0.73
```

## Deploy Wordpress

Build and deploy the Wordpress instance.
The `WORDPRESS_DB_HOST` environment variable tells WordPress where to reach
MariaDB and must match the internal domain assigned to the MariaDB instance.
It defaults to `wordpress-mariadb.internal`.

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./wordpress --output <my-org>/wordpress:latest
unikraft run --name wordpress --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:8080/tls+http -m 2G --volume wordpress-wordpress-data:/var/www/html --image <my-org>/wordpress:latest --env WORDPRESS_DB_HOST=wordpress-mariadb.internal
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --name wordpress --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:8080/tls+http -M 2Gi --volume wordpress-wordpress-data:/var/www/html --env WORDPRESS_DB_HOST=wordpress-mariadb.internal ./wordpress/
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:                     fra
name:                      wordpress
uuid:                      ee9f5599-b33b-44f1-ab57-3871b440e810
state:                     starting
image:                     <my-org>/wordpress
runtime:
  env:
    WORDPRESS_DB_HOST:     wordpress-mariadb.internal
resources:
  memory:                  2GiB
  vcpus:                   1
service:
  name:                    damp-lake-n09gzguc
  uuid:                    7f21d778-487f-4130-a94a-34b86862c3dd
  domains:
  - fqdn:                  damp-lake-n09gzguc.fra.unikraft.app
volumes:
- name:                    wordpress-wordpress-data
  uuid:                    0bec8b93-0691-43b6-b188-4ac170a3d0c7
  at:                      /var/www/html
networks:
- uuid:                    e0f13623-fd04-4a69-9caf-47142ce47c4c
  private-ip:              10.0.0.33
  mac:                     12:b0:0a:00:00:21
timestamps:
  created:                 just now
scale-to-zero:
  enabled:                 true
  policy:                  on
  cooldown-time:           1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: wordpress
 ├───────── uuid: ee9f5599-b33b-44f1-ab57-3871b440e810
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://damp-lake-n09gzguc.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/wordpress@sha256:b43...
 ├─────── memory: 2048 MiB
 ├────── service: damp-lake-n09gzguc
 ├─ private fqdn: wordpress.internal
 └─── private ip: 10.0.0.33
```

Use a browser to access the install page of Wordpress using the URL from the `fqdn` field in the output.
Fill out the form and complete the Wordpress install.

You can list information about the instances by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instance list
```

```ansi title="unikraft"
METRO  NAME       STATE    IMAGE               ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    mariadb    standby  <my-org>/mariadb          1GiB    1      wordpress-mariadb.internal           5 minutes ago
fra    wordpress  running  <my-org>/wordpress        2GiB    1      damp-lake-n09gzguc.fra.unikraft.app  1 minute ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME       FQDN                                 STATE    STATUS       IMAGE                                             MEMORY   VCPUS  ARGS  BOOT TIME
wordpress  damp-lake-n09gzguc.fra.unikraft.app  running  since 1min   oci://unikraft.io/<my-org>/wordpress@sha256:b...  2.0 GiB  1            6873.49 ms
mariadb    wordpress-mariadb.internal           running  since 7mins  oci://unikraft.io/<my-org>/mariadb@sha256:cf1...  1.0 GiB  1            2505.65 ms
```

When done, you can remove the instances and volumes:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete mariadb wordpress
unikraft volume delete wordpress-wordpress-data wordpress-db-data
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove mariadb wordpress
kraft cloud volume remove wordpress-wordpress-data wordpress-db-data
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft --help
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
