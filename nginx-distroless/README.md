# Distroless Nginx

This example uses [`Nginx`](https://nginx.org), one of the most popular web servers.
Nginx can be used with Unikraft / Unikraft Cloud to serve static web content.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/nginx-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/nginx-distroless/
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

When done, invoke the following command to deploy this app on Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/nginx-distroless:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/nginx-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 256Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:           fra
name:            nginx-distroless-67zbu
uuid:            8a8bc1b9-0af6-420e-a426-190dc2da9eaa
state:           starting
image:           <my-org>/nginx-distroless
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

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: nginx-distroless-67zbu
 ├───────── uuid: 8a8bc1b9-0af6-420e-a426-190dc2da9eaa
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://nameless-fog-0tvh1uov.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/nginx-distroless@sha256:f51ecc121c9ca34abb88a2bc6a69765501304f7893f7e85af15fbec3dc86e2bd
 ├─────── memory: 256 MiB
 ├────── service: nameless-fog-0tvh1uov
 ├─ private fqdn: nginx-distroless-67zbu.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `nginx-distroless-67zbu` and the address is `https://nameless-fog-0tvh1uov.fra.unikraft.app`.
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

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                    STATE    IMAGE                      ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    nginx-distroless-67zbu  running  <my-org>/nginx-distroless        256MiB  1      nameless-fog-0tvh1uov.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                    FQDN                                    STATE    STATUS         IMAGE
MEMORY   VCPUS  ARGS  BOOT TIME
nginx-distroless-67zbu  nameless-fog-0tvh1uov.fra.unikraft.app  running  5 minutes ago  oci://unikraft.io/<my-org>/nginx-distroless@sha256:...  256 MiB  1            11.13 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete nginx-distroless-67zbu
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove nginx-distroless-67zbu
```

## Customize your app

To customize the Nginx app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `rootfs/wwwroot/index.html`: the index page of the content served
* `rootfs/etc/nginx/nginx.conf`: the Nginx configuration file

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

If required, you can also customize the configuration of Nginx in `rootfs/etc/nginx/nginx.conf`.
You can set a new webroot (different than `wwwroot`), or a different internal port, or a different index page, etc.

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
