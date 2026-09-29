# DragonflyDB

This guide shows you how to deploy [Dragonfly](https://www.dragonflydb.io/), a simple, performant, and cost-efficient in-memory data store.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/dragonflydb/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/dragonflydb/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/dragonflydb:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:6379/http+tls \
  --scale-to-zero policy=off \
  --image <my-org>/dragonflydb:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         dragonflydb-10zgk
uuid:         6282ef0c-2161-494c-a3f3-2d16055096c2
state:        starting
image:        <my-org>/dragonflydb
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       18326b44-a571-6195-b9e6-9368832ff2b3
  name:       dry-moon-x6bgl6c0
  domains:
  - fqdn:     dry-moon-x6bgl6c0.fra.unikraft.app
networks:
- uuid:       87aa7a40-2a83-f315-b656-e07a8637af64
  private-ip: 10.0.6.5
  mac:        12:b0:8f:c2:51:55
timestamps:
  created:    just now
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

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME               STATE    IMAGE                 ARGS  MEMORY  VCPUS  FQDN                                CREATED
fra    dragonflydb-10zgk  running  <my-org>/dragonflydb        512MiB  1      dry-moon-x6bgl6c0.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete dragonflydb-10zgk
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
