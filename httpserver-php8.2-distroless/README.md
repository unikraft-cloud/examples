# Distroless PHP HTTP Server

This guide explains how to create and deploy a simple PHP-based HTTP web server.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-php8.2-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-php8.2-distroless/
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
unikraft build . --output <my-org>/httpserver-php82-distroless:latest
unikraft run --metro fra \
  -m 512M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-php82-distroless:latest
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
name:         httpserver-php82-distroless-g00si
uuid:         033b2f4b-72ff-414d-b0de-63571477c657
state:        starting
image:        <my-org>/httpserver-php82-distroless
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       a6f268b1-05c3-31c1-7d9b-76cb952fd713
  name:       aged-fire-rh0oi0tj
  domains:
  - fqdn:     aged-fire-rh0oi0tj.fra.unikraft.app
networks:
- uuid:       f18bc9d1-a75d-dbd0-6566-599c2a1a95a6
  private-ip: 10.0.3.3
  mac:        12:b0:af:34:d3:e8
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-php82-distroless-g00si
 ├───────── uuid: 033b2f4b-72ff-414d-b0de-63571477c657
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://aged-fire-rh0oi0tj.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-php82-distroless@sha256:dccaac053982673765b8f00497a9736c31458ab23ad59a550b09aa8dedfabb34
 ├─────── memory: 512 MiB
 ├────── service: aged-fire-rh0oi0tj
 ├─ private fqdn: httpserver-php82-distroless-g00si.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `httpserver-php82-distroless-g00si` and the address is `https://aged-fire-rh0oi0tj.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the PHP-based HTTP web server:

```bash
curl https://aged-fire-rh0oi0tj.fra.unikraft.app
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
METRO  NAME                               STATE    IMAGE                                 ARGS  MEMORY  VCPUS  FQDN
     CREATED
fra    httpserver-php82-distroless-g00si  running  <my-org>/httpserver-php82-distroless        512MiB  1      aged-fire-rh0oi0tj.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                               FQDN                                 STATE    STATUS          IMAGE
                                        MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-php82-distroless-g00si  aged-fire-rh0oi0tj.fra.unikraft.app  running  50 seconds ago  oci://unikraft.io/<my-org>/httpserver-php82-distroless@sha256:...  512 MiB  1            32.80 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-php82-distroless-g00si
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-php82-distroless-g00si
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.php`: the actual PHP HTTP server implementation
* `php.ini`: the PHP configuration
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `server.php` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.
  If you need new extensions, that may require updating the `php.ini` file.

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
