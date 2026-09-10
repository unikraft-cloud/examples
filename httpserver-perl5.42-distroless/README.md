# Distroless Perl HTTP Server

This guide explains how to create and deploy a simple Perl-based HTTP web server.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-perl5.42-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-perl5.42-distroless/
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
unikraft build . --output <my-org>/httpserver-perl542-distroless:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-perl542-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 512Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-perl542-distroless-xue8j
uuid:         59d08bbc-cbb7-4c6b-a2cb-847828845db9
state:        starting
image:        <my-org>/httpserver-perl542-distroless
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       b62c0c0a-2de6-9068-1e93-223fa8f1edbf
  name:       fragrant-water-wau08gaw
  domains:
  - fqdn:     fragrant-water-wau08gaw.fra.unikraft.app
networks:
- uuid:       22bdfc9c-2f69-eb7e-5b5e-929aba51a2c0
  private-ip: 10.0.1.161
  mac:        12:b0:d4:aa:c1:98
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-perl542-distroless-xue8j
 ├───────── uuid: 59d08bbc-cbb7-4c6b-a2cb-847828845db9
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://fragrant-water-wau08gaw.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-perl542-distroless@sha256:af86e8f03c0d4cfd596ccfd9a9d18ea75ac68c996c9cde31f64db24dc11100fe
 ├─────── memory: 512 MiB
 ├────── service: fragrant-water-wau08gaw
 ├─ private fqdn: httpserver-perl542-distroless-xue8j.internal
 └─── private ip: 10.0.1.161
```

In this case, the instance name is `httpserver-perl542-distroless-xue8j` and the address is `https://fragrant-water-wau08gaw.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Perl-based HTTP web server:

```bash
curl https://fragrant-water-wau08gaw.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                 STATE    IMAGE                                   ARGS  MEMORY  VCPUS  FQDN
              CREATED
fra    httpserver-perl542-distroless-xue8j  standby  <my-org>/httpserver-perl542-distroless        512MiB  1      fragrant-water-wau08gaw.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                 FQDN                                      STATE    STATUS   IMAGE
                                          MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-perl542-distroless-xue8j  fragrant-water-wau08gaw.fra.unikraft.app  standby  standby  oci://unikraft.io/<my-org>/httpserver-perl542-distroless@sha256:...  512 MiB  1            109.46 ms
```

When you list your instances, you might notice they show as standby.
This is normal behavior and means the instance is using Unikraft Cloud's scale-to-zero feature that saves resources when there is no traffic.
To check your instance is working, open two terminals and use these commands to watch the status:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instance list --watch
# In another terminal, make requests
curl https://fragrant-water-wau08gaw.fra.unikraft.app
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
watch -n 1 "kraft cloud instance list"
# In another terminal, make requests
curl https://fragrant-water-wau08gaw.fra.unikraft.app
```

It switches to "running" then back to "standby."

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-perl542-distroless-xue8j
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-perl542-distroless-xue8j
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.pl`: the actual Perl HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `server.pl` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

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
