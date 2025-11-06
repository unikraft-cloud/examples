# NGINX

This example uses [`Nginx`](https://nginx.org), one of the most popular web servers.
Nginx can be used with Unikraft / Unikraft Cloud to serve static web content.

To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/nginx/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/nginx/
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
kraft cloud deploy -p 443:8080 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: nginx-67zbu
 ├────────── uuid: 8a8bc1b9-0af6-420e-a426-190dc2da9eaa
 ├───────── state: running
 ├─────────── url: https://nameless-fog-0tvh1uov.fra.unikraft.app
 ├───────── image: nginx@sha256:f51ecc121c9ca34abb88a2bc6a69765501304f7893f7e85af15fbec3dc86e2bd
 ├───── boot time: 11.13ms
 ├──────── memory: 128 MiB
 ├─────── service: nameless-fog-0tvh1uov
 ├── private fqdn: nginx-67zbu.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/nginx -c /etc/nginx/nginx.conf
```

In this case, the instance name is `nginx-67zbu` and the address is `https://nameless-fog-0tvh1uov.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Nginx.

```bash
curl https://nameless-fog-0tvh1uov.fra.unikraft.app
```
```text
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
[...]
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME         FQDN                                    STATE    STATUS         IMAGE                               MEMORY   VCPUS  ARGS                                     BOOT TIME
nginx-67zbu  nameless-fog-0tvh1uov.fra.unikraft.app  running  5 minutes ago  nginx@sha256:f51ecc121c9ca34abb...  128 MiB  1      /usr/bin/nginx -c /etc/nginx/nginx.conf  11129us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove nginx-67zbu
```

## Customize your app

To customize the Nginx app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `rootfs/wwwroot/index.html`: the index page of the content served
* `rootfs/conf/nginx.conf`: the Nginx configuration file

Update the contents of the `rootfs/wwwroot/` directory to serve different static web content.
For example, you could change the contents of `rootfs/wwwroot/index.html` to:

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

After re-deploying the Nginx image on Unikraft Cloud, using `curl` or a browser to query it will present the new page contents.

Tools like [`Jekyll`](https://jekyllrb.com/) or [`Hugo`](https://gohugo.io/) can generate the static web content located in the `rootfs/wwwroot/` offline.

If required, you can also customize the configuration of Nginx in `rootfs/conf/nginx.conf`.
You can set a new webroot (different than `wwwroot`), or a different internal port, or a different index page, etc.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
