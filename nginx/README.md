# Nginx

This example uses [`Nginx`](https://nginx.org), one of the most popular web servers.
Nginx can be used with Unikraft / Unikraft Cloud to serve static web content.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/nginx/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/nginx/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/nginx:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/nginx:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:           fra
name:            nginx-67zbu
uuid:            8a8bc1b9-0af6-420e-a426-190dc2da9eaa
state:           starting
image:           <my-org>/nginx
resources:
  memory:        256MiB
  vcpus:         1
service:
  uuid:          a942b9b5-ad17-3ffe-dcd2-ef4331f9087a
  name:          nameless-fog-0tvh1uov
  domains:
  - fqdn:        nameless-fog-0tvh1uov.fra.unikraft.app
networks:
- uuid:          62d9bbf0-aec8-61f6-7bdb-86edf63dd068
  private-ip:    10.0.3.3
  mac:           12:b0:c6:23:ed:15
timestamps:
  created:       just now
scale-to-zero:
  enabled:       true
  policy:        on
  cooldown-time: 1s
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

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME         STATE    IMAGE           ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    nginx-67zbu  running  <my-org>/nginx        256MiB  1      nameless-fog-0tvh1uov.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete nginx-67zbu
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

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
