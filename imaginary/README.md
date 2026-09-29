# Imaginary

This example uses [`imaginary`](https://github.com/h2non/imaginary), an HTTP microservice for high-level image processing.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/imaginary/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/imaginary/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/imaginary:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/imaginary:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         imaginary-mwb4y
uuid:         8cf18bf7-2bf6-4f23-be07-f9c234c7962d
state:        starting
image:        <my-org>/imaginary
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       b9b7fa60-5f4f-13e5-41e9-eeea476f4398
  name:       divine-wind-1ycjvhqs
  domains:
  - fqdn:     divine-wind-1ycjvhqs.fra.unikraft.app
networks:
- uuid:       91467bd9-8d52-a378-4426-7014ca09e5d5
  private-ip: 10.0.3.3
  mac:        12:b0:e2:ed:95:49
timestamps:
  created:    just now
```

In this case, the instance name is `imaginary-mwb4y` and the address is `https://divine-wind-1ycjvhqs.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Imaginary.
You will get a health status of the service:

```bash
curl -s https://divine-wind-1ycjvhqs.fra.unikraft.app/health | jq
```

```json
{
  "uptime": 414,
  "allocatedMemory": 0.19,
  "totalAllocatedMemory": 0.72,
  "goroutines": 6,
  "completedGCCycles": 13,
  "cpus": 1,
  "maxHeapUsage": 3.63,
  "heapInUse": 0.19,
  "objectsInUse": 846,
  "OSMemoryObtained": 7.73
}
```

To test the Imaginary instance on Unikraft Cloud use the `/form` endpoint.
That is, open the `https://divine-wind-1ycjvhqs.fra.unikraft.app/form` address in the browser and use the existing forms to process an image.

To make actual use of the Imaginary instance, use [the endpoints of the HTTP API](https://github.com/h2non/imaginary/blob/master/README.md#get).
The API provides endpoints, together with parameters, for different image processing options: `/crop`, `/resize`, `/flip`, `/convert`, `/watermark`, `/rotate`, `/blur` etc.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME             STATE    IMAGE               ARGS  MEMORY  VCPUS  FQDN                                   CREATED
fra    imaginary-mwb4y  running  <my-org>/imaginary        512MiB  1      divine-wind-1ycjvhqs.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete imaginary-mwb4y
```

The Imaginary Unikraft Cloud service works as is: you deploy it and then you query [the endpoints of the HTTP API](https://github.com/h2non/imaginary/blob/master/README.md#get).
You can customize the command line options used to start the service, by updating the `cmd` line in the `Kraftfile`:

```yaml
spec: v0.7

runtime: base-compat:latest

cmd: ["/usr/bin/imaginary", "-p", "8080"]
```

You can update the `cmd` line with [command line option for Imaginary](https://github.com/h2non/imaginary/blob/master/README.md#command-line-usage).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
