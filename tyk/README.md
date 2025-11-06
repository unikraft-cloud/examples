# Tyk

This example uses [`Tyk`](https://tyk.io/), an API gateway and management platform.
Tyk is used together with Redis to store API tokens and OAuth clients.

To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/tyk/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/tyk/
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
kraft cloud compose up
```

The output shows the [Compose](/docs/guides/features/compose) output:

```text
 i  building service=tyk
 i  packaging service=tyk
[+] building rootfs... done!
[+] packaging index.unikraft.io/tyk-tyk... done!
[+] pushing index.unikraft.io/tyk-tyk:latest (kraftcloud/x86_64)... done!
 i  creating instance image=redis:latest
 i  no ports or service specified, disabling scale to zero
 i  creating instance image=index.unikraft.io/tyk-tyk@sha256:06f8ba3f2350e57717bd947f43f04a1ac44ab65010c8994488223eb042c30feb
 i  no ports or service specified, disabling scale to zero
 i  starting 2 instance(s)
```

To list information about the instances, use:

```bash
kraft cloud compose ps
```
```ansi
NAME       FQDN                                  STATE    STATUS        IMAGE                                             MEMORY   VCPUS  ARGS                                         BOOT TIME
tyk-tyk    funky-pond-45usfkxx.fra.unikraft.app  running  since 45secs  tyk-tyk@sha256:06f8ba329fd9d9100skf1721fe...      128 MiB  1      /usr/bin/tyk start --conf /etc/tyk.conf      38.12 ms
tyk-redis                                        running  since 45secs  tyk-redis@sha256:d4604c6d80e7d57590f2c46659f2...  512 MiB  1      /usr/bin/redis-server /etc/redis/redis.conf  18.69 ms
```

The Tyk and Redis instances are named `tyk-tyk` and `tyk-redis` (as defined in the `compose.yaml` file).
Only the Tyk instance is available as a public service.
Its address is `https://funky-pond-45usfkxx.fra.unikraft.app`.
It's different for each run.

Use `curl` to query the Tyk instance on Unikraft Cloud on the available address:

```bash
curl https://funky-pond-45usfkxx.fra-test.unikraft.app/hello
```
```text
{"status":"pass","version":"v5.3.0-dev","description":"Tyk GW","details":{"redis":{"status":"pass","componentType":"datastore","time":"2024-07-12T05:57:44Z"}}}
```

When done, you can bring down the instances:

```bash
kraft cloud compose down
```

## Customize your app

To customize the Tyk app, you can update:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile` / `rootfs/`: the Tyk filesystem (in this case the configuration file `/etc/tyk.conf`)
* `compose.yaml`: the Compose specification

It's unlikely you will have to update the `Kraftfile` specification.

Update the contents of the `rootfs/etc/tyk.conf` file for a different configuration.

You can also update the `Dockerfile` in order to extend the Tyk filesystem with extra data files or configuration files.

The `compose.yaml` file can be update to assign different names, ports, network names or other [Compose](/docs/guides/features/compose)-specific configurations.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
