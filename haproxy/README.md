# HAProxy

This guide shows you how to use [HAProxy](https://www.haproxy.org).
HAProxy is a free and open source software that provides a high availability load balancer and reverse proxy for TCP and HTTP-based apps that spreads requests across many servers.

To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/haproxy/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/haproxy/
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
kraft cloud deploy -p 443:8404 -M 256 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: haproxy-rfx6z
 ├────────── uuid: 09bd081e-e082-4f73-8ba8-531123a39e2e
 ├───────── state: running
 ├─────────── url: https://cool-paper-svzzr3qq.fra.unikraft.app
 ├───────── image: haproxy@sha256:32296847231c151506820ec4914c1d7416e5b7200caf07c1e40eaa3ea5033d21
 ├───── boot time: 26.60 ms
 ├──────── memory: 256 MiB
 ├─────── service: cool-paper-svzzr3qq
 ├── private fqdn: haproxy-rfx6z.internal
 ├──── private ip: 172.16.6.5
 └────────── args: /usr/bin/haproxy -f /etc/haproxy/haproxy.conf
```

In this case, the instance name is `haproxy-rfx6z` and the address is `https://cool-paper-svzzr3qq.fra.unikraft.app`.
They're different for each run.

To test, point your browser at the `/stats` endpoint (for example, `https://cool-paper-svzzr3qq.fra.unikraft.app/stats`).

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME           FQDN                                  STATE    STATUS        IMAGE                               MEMORY   VCPUS  ARGS                               BOOT TIME
haproxy-rfx6z  cool-paper-svzzr3qq.fra.unikraft.app  running  1 minute ago  haproxy@sha256:32296847231c1515...  256 MiB  1      /usr/bin/haproxy -f /etc/hapro...  26596us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove haproxy-rfx6z
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
