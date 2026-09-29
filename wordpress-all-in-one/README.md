# Wordpress

This guide shows you how to use [Wordpress](https://wordpress.com/), a web content management system.

To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/wordpress-all-in-one/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/wordpress-all-in-one/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/wordpress-all-in-one:latest
unikraft run --metro fra \
  -m 4G \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=3000,stateful=true \
  --image <my-org>/wordpress-all-in-one:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         wordpress-fx5rb
uuid:         bfb9d151-1604-452a-b2e0-f737486744df
state:        starting
image:        <my-org>/wordpress
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       398fe5bb-e172-465e-8f74-56ffcfb24a3d
  name:       cool-silence-h5c1es4z
  domains:
  - fqdn:     cool-silence-h5c1es4z.fra.unikraft.app
networks:
- uuid:       26c200e0-43eb-dd46-e4be-e9505ff677d1
  private-ip: 10.0.3.1
  mac:        12:b0:4e:20:b3:e7
timestamps:
  created:    just now
```

In this case, the instance name is `wordpress-fx5rb`.
They're different for each run.

Use a browser to access the install page of Wordpress.
Fill out the form and complete the Wordpress install.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME             STATE    IMAGE                          ARGS  MEMORY   VCPUS  FQDN                                    CREATED
fra    wordpress-fx5rb  running  <my-org>/wordpress-all-in-one        4096MiB  1      cool-silence-h5c1es4z.fra.unikraft.app  1 minute ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete wordpress-fx5rb
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
