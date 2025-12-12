# DragonflyDB

This guides shows you how to deploy [Dragonfly](https://www.dragonflydb.io/), a simple, performant, and cost-efficient in-memory data store.

To run it example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/dragonflydb/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/dragonflydb/
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
kraft cloud deploy -p 443:6379 -M 512 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: dragonflydb-10zgk
 ├────────── uuid: 6282ef0c-2161-494c-a3f3-2d16055096c2
 ├───────── state: running
 ├─────────── url: https://dry-moon-x6bgl6c0.fra.unikraft.app
 ├───────── image: dragonflydb@sha256:21e6d3ff1f86292e14266bcf5c6e73d3b7a86a0ec4102c66a0961373af743f19
 ├───── boot time: 28.74 ms
 ├──────── memory: 512 MiB
 ├─────── service: dry-moon-x6bgl6c0
 ├── private fqdn: dragonflydb-10zgk.internal
 ├──── private ip: 172.16.6.5
 └────────── args: /usr/bin/dragonfly --maxmemory 256MiB
```

In this case, the instance name is `dragonflydb-10zgk` and the address is `https://dry-moon-x6bgl6c0.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Drangonfly.

```bash
curl https://dry-moon-x6bgl6c0.fra.unikraft.app
```
```html
<!DOCTYPE html>
<html><head>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
    <link href='https://fonts.googleapis.com/css?family=Roboto:400,300' rel='stylesheet'
     type='text/css'>
    <link rel='stylesheet' href='http://static.dragonflydb.io/data-plane/status_page.css'>
    <script type="text/javascript" src="http://static.dragonflydb.io/data-plane/status_page.js"></script>
</head>
<body>
<div><img src='http://static.dragonflydb.io/data-plane/logo.png' width="160"/></div>
<div class='left_panel'></div>
<div class='styled_border'>
<div>Status:<span class='key_text'>OK</span></div>
<div>Started on:<span class='key_text'>1970-01-01T00:00:00</span></div>
<div>Uptime:<span class='key_text'>474611:3:38</span></div>
<div>Render Latency:<span class='key_text'>110 us</span></div>
</div>
</body>
<script>
var json_text1 = {"engine": { "keys": 0,"obj_mem_usage": 0,"table_load_factor": 0 },
"current-time": 1708599818};
document.querySelector('.left_panel').innerHTML = JsonToHTML(json_text1);
</script>
</html>
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME               FQDN                                STATE    STATUS        IMAGE                         MEMORY   VCPUS  ARGS                              BOOT TIME
dragonflydb-10zgk  dry-moon-x6bgl6c0.fra.unikraft.app  running  1 minute ago  dragonflydb@sha256:21e6d3...  512 MiB  1      /usr/bin/dragonfly --maxmemor...  28740us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove dragonflydb-10zgk
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
