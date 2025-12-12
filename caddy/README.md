# Caddy

This example uses [`Caddy`](https://caddyserver.com/), one of the most popular web servers.
Caddy can be used with Unikraft / Unikraft Cloud to serve static web content.

To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/caddy/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/caddy/
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
kraft cloud deploy -p 443:2015 -M 256 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: caddy-vhf4m
 ├────────── uuid: db624eff-4739-4500-873c-f7c58e4eefd7
 ├───────── state: running
 ├─────────── url: https://frosty-sky-vz8kwsmb.fra.unikraft.app
 ├───────── image: caddy@sha256:25df97e3c43147c683f31dd062d0fa75122358b596de5804ca246c4e8613dd56
 ├───── boot time: 20.18ms
 ├──────── memory: 256 MiB
 ├─────── service: frosty-sky-vz8kwsmb
 ├── private fqdn: caddy-vhf4m.internal
 ├──── private ip: 172.16.6.2
 └────────── args: /usr/bin/caddy run --config /etc/caddy/Caddyfile
```

In this case, the instance name is `caddy-vhf4m` and the address is `https://frosty-sky-vz8kwsmb.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Caddy.

```bash
curl https://frosty-sky-vz8kwsmb.fra.unikraft.app
```
```text
Hello World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME         FQDN                                  STATE    STATUS        IMAGE                               MEMORY   VCPUS  ARGS                               BOOT TIME
caddy-vhf4m  frosty-sky-vz8kwsmb.fra.unikraft.app  running  1 minute ago  caddy@sha25:25df97e3c43147c683f...  256 MiB  1      /usr/bin/caddy run --config /e...  20180us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove caddy-vhf4m
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `rootfs/var/www/index.html`: the index page of the content served
* `rootfs/etc/caddy/Caddyfile`: the Caddy configuration file

Update the contents of the `rootfs/var/www` directory to serve different static web content.
For example, you could change the contents of `rootfs/var/www/index.html` to:

```html
<!DOCTYPE html>
<html>
<head>
<title>Hello</title>
</head>
<body>
<h2>Hello, World!</h2>
</body>
</html>
```

After re-deploying the Caddy image on Unikraft Cloud, using `curl` or a browser to query it will present the new page contents.

You can generate the static web content in `rootfs/var/www/` offline with tools such as [`Jekyll`](https://jekyllrb.com/) or [`Hugo`](https://gohugo.io/).

If required, you can also customize the configuration of Caddy in `rootfs/etc/caddy/Caddyfile`.
You can set a new webroot (different than `rootfs`), or a different internal port, or a different index page, etc.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
