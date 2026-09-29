# Minio

This guide shows you how to use [MinIO](https://min.io), a High Performance Object Storage which is
Open Source, Amazon S3 compatible, Kubernetes Native and works for cloud native workloads like AI.

To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/minio/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/minio/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/minio:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:9001/tls+http \
  -p 9000:9000/tls \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/minio:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         minio-w2my8
uuid:         31e691ad-05a0-48b6-ad49-7f79da8e1754
state:        starting
image:        <my-org>/minio
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       8fdad5ff-9276-5f35-f94e-3d9d9b244a15
  name:       icy-bird-tregaga9
  domains:
  - fqdn:     icy-bird-tregaga9.fra.unikraft.app
networks:
- uuid:       f3a7d1f6-b1ca-68d0-6b45-7e9179ad0966
  private-ip: 10.0.6.4
  mac:        12:b0:44:5e:b0:54
timestamps:
  created:    just now
```

In this case, the instance name is `minio-w2my8` and the address is `https://icy-bird-tregaga9.fra.unikraft.app`.
They're different for each run.

To test, point your browser at the address.
The default account/password are `minioadmin/minioadmin`.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME         STATE    IMAGE           ARGS  MEMORY  VCPUS  FQDN                                CREATED
fra    minio-w2my8  running  <my-org>/minio        512MiB  1      icy-bird-tregaga9.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete minio-w2my8
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
