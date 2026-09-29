# Hugo

This guide shows you how to use [Hugo](https://gohugo.io/commands/hugo_server/), a high performance webserver, with the [ananke](https://github.com/budparr/gohugo-theme-ananke.git) theme.

To run it, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/hugo0.122/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/hugo0.122/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/hugo0122:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:1313/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/hugo0122:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         hugo0122-zpabu
uuid:         dfc6e06c-76cc-4aa1-a053-c4eded0d2456
state:        starting
image:        <my-org>/hugo0122
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       f5492054-269e-2bcb-1d6c-18b2129c423a
  name:       morning-rain-jikpfy3t
  domains:
  - fqdn:     morning-rain-jikpfy3t.fra.unikraft.app
networks:
- uuid:       4dd794e8-ee05-6d97-fdc8-b86f92dc1b44
  private-ip: 10.0.6.4
  mac:        12:b0:fe:77:90:47
timestamps:
  created:    just now
```

In this case, the instance name is `hugo0122-zpabu` and the address is `https://morning-rain-jikpfy3t.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Hugo.

```bash
curl https://morning-rain-jikpfy3t.fra.unikraft.app
```

```html
<!DOCTYPE html>
<html lang="en-us">
  <head><script src="/livereload.js?mindelay=10&amp;v=2&amp;port=1313&amp;path=livereload" data-no-instant defer></script>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
[...]
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME            STATE    IMAGE              ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    hugo0122-zpabu  running  <my-org>/hugo0122        512MiB  1      morning-rain-jikpfy3t.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete hugo0122-zpabu
```

## Customize your app

To customize the Hugo app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `site/`: sample site content
* `Dockerfile`: In case you need to add files to your instance's rootfs

Update the contents of the `site/` directory to serve different static web content.

After re-deploying the Hugo image on Unikraft Cloud, using `curl` or a browser to query it will present the new page contents.

Tools like [`Jekyll`](https://jekyllrb.com/) or [`Hugo`](https://gohugo.io/) can generate the static web content located in the `site/` offline.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
