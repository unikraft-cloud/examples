# Imaginary

This example uses [`imaginary`](https://github.com/h2non/imaginary), an HTTP microservice for high-level image processing.

To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/imaginary/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/imaginary/
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
kraft cloud deploy -p 443:8080 -M 256 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: imaginary-mwb4y
 ├────────── uuid: 8cf18bf7-2bf6-4f23-be07-f9c234c7962d
 ├───────── state: running
 ├─────────── url: https://divine-wind-1ycjvhqs.fra.unikraft.app
 ├───────── image: imaginary@sha256:673834bc531038bb621266f7fd635a04e559050cbe82876df811fd4b975ea4fe
 ├───── boot time: 32.26 ms
 ├──────── memory: 256 MiB
 ├─────── service: divine-wind-1ycjvhqs
 ├── private fqdn: imaginary-mwb4y.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/imaginary -p 8080
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

```bash
kraft cloud instance list
```
```ansi
NAME             FQDN                                   STATE    STATUS          IMAGE                                         MEMORY   VCPUS  ARGS                        BOOT TIME
imaginary-mwb4y  divine-wind-1ycjvhqs.fra.unikraft.app  running  54 seconds ago  imaginary@sha256:673834bc531038bb621266f7...  256 MiB  1      /usr/bin/imaginary -p 8080  32262us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove imaginary-mwb4y
```

The Imaginary Unikraft Cloud service works as is: you deploy it and then you query [the endpoints of the HTTP API](https://github.com/h2non/imaginary/blob/master/README.md#get).
You can customize the command line options used to start the service, by updating the `cmd` line in the `Kraftfile`:

```yaml
spec: v0.6

runtime: imaginary:1.2

cmd: ["/usr/bin/imaginary", "-p", "8080"]
```

You can update the `cmd` line with [command line option for Imaginary](https://github.com/h2non/imaginary/blob/master/README.md#command-line-usage).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
