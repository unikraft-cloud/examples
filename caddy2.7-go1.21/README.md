# Caddy

This example uses [`Caddy`](https://caddyserver.com/), one of the most popular web servers.
Caddy can be used with Unikraft / Unikraft Cloud to serve static web content.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/caddy2.7-go1.21/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/caddy2.7-go1.21/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/caddy27-go121:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:2015/http+tls \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/caddy27-go121:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         caddy27-go121-vhf4m
uuid:         db624eff-4739-4500-873c-f7c58e4eefd7
state:        starting
image:        <my-org>/caddy27-go121
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       085cfc91-34d2-0e4d-5f19-fe67832f16a8
  name:       frosty-sky-vz8kwsmb
  domains:
  - fqdn:     frosty-sky-vz8kwsmb.fra.unikraft.app
networks:
- uuid:       a72ea1ab-9686-c5b5-a8c2-fd58922f30f3
  private-ip: 10.0.6.2
  mac:        12:b0:a9:b2:fd:13
timestamps:
  created:    just now
```


In this case, the instance name is `caddy27-go121-vhf4m` and the address is `https://frosty-sky-vz8kwsmb.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Caddy.

```bash
curl https://frosty-sky-vz8kwsmb.fra.unikraft.app
```

```text
Hello World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                 STATE    IMAGE                   ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    caddy27-go121-vhf4m  running  <my-org>/caddy27-go121        256MiB  1      frosty-sky-vz8kwsmb.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete caddy27-go121-vhf4m
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

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
