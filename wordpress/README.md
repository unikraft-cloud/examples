# Wordpress with Nginx and MariaDB

This guide explains how to create and deploy a Wordpress app with Nginx and MariaDB.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/wordpress` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/wordpress/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

## Create Volumes

Create the volumes for the Wordpress and MariaDB data:

```bash title="unikraft"
unikraft volume create --metro fra --name wordpress-wordpress-data --size 512M
unikraft volume create --metro fra --name wordpress-db-data --size 512M
```

You can list the created volumes by running:

```bash title="unikraft"
unikraft volume list
```

```ansi title="unikraft"
METRO  NAME                      STATE      SIZE    CREATED
fra    wordpress-db-data         available  512MiB  just now
fra    wordpress-wordpress-data  available  512MiB  just now
```

## Deploy MariaDB

Build and deploy the MariaDB instance.
MariaDB is an internal service (not publicly accessible), reached via the `wordpress-mariadb.internal` domain:

```bash title="unikraft"
unikraft build ./mariadb --output <my-org>/mariadb:latest
unikraft run --metro fra \
  --name mariadb \
  -m 1G \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --domain wordpress-mariadb.internal \
  --env MARIADB_ROOT_PASSWORD=unikraft \
  --volume wordpress-db-data:/var/lib/mysql \
  --image <my-org>/mariadb:latest
```

Make sure to replace `<my-org>` with your username / org-name.

The output shows the instance details:

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

## Deploy Wordpress

Build and deploy the Wordpress instance.
Set `WORDPRESS_DB_HOST` to the same internal domain you assigned to the MariaDB instance (`wordpress-mariadb.internal` in this guide).

```bash title="unikraft"
unikraft build ./wordpress --output <my-org>/wordpress:latest
unikraft run --metro fra \
  --name wordpress \
  -m 2G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --env WORDPRESS_DB_HOST=wordpress-mariadb.internal \
  --volume wordpress-wordpress-data:/var/www/html \
  --image <my-org>/wordpress:latest
```

The output shows the instance address and other details:

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

Use a browser to access the install page of Wordpress using the URL from the `fqdn` field in the output.
Fill out the form and complete the Wordpress install.

You can list information about the instances by running:

```bash title="unikraft"
unikraft instance list
```

```ansi title="unikraft"
METRO  NAME       STATE    IMAGE               ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    mariadb    standby  <my-org>/mariadb          1GiB    1      wordpress-mariadb.internal           5 minutes ago
fra    wordpress  running  <my-org>/wordpress        2GiB    1      damp-lake-n09gzguc.fra.unikraft.app  1 minute ago
```

When done, you can remove the instances and volumes:

```bash title="unikraft"
unikraft instances delete mariadb wordpress
unikraft volume delete wordpress-wordpress-data wordpress-db-data
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
