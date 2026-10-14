# Distroless Flask and SQLite HTTP Server

This guide explains how to create and deploy a Python Flask app using SQLite.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-python3.12-flask3.0-sqlite-distroless/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-python3.12-flask3.0-sqlite-distroless/
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
unikraft build . --output <my-org>/httpserver-python312-flask30-sqlite-distroless:latest
unikraft run --metro fra \
  -m 768M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-python312-flask30-sqlite-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 768Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-python312-flask30-sqlite-distroless-qodkd
uuid:         e00e7aca-962d-409c-87c2-c245ca08b54b
state:        starting
image:        <my-org>/httpserver-python312-flask30-sqlite-distroless
resources:
  memory:     768MiB
  vcpus:      1
service:
  uuid:       1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d
  name:       lingering-orangutan-840mmdvd
  domains:
  - fqdn:     lingering-orangutan-840mmdvd.fra.unikraft.app
networks:
- uuid:       2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e
  private-ip: 10.0.3.3
  mac:        12:b0:8a:4f:2c:91
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-python312-flask30-sqlite-distroless-qodkd
 ├───────── uuid: e00e7aca-962d-409c-87c2-c245ca08b54b
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://lingering-orangutan-840mmdvd.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-python312-flask30-sqlite-distroless@sha256:bdb0bf35a9675b9b3836cbb626606da0606334d91768c7ba31195c3062d6f517
 ├─────── memory: 768 MiB
 ├────── service: lingering-orangutan-840mmdvd
 ├─ private fqdn: httpserver-python312-flask30-sqlite-distroless-qodkd.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `httpserver-python312-flask30-sqlite-distroless-qodkd` and the address is `https://lingering-orangutan-840mmdvd.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Python-based HTTP web server:

```bash
curl https://young-night-5fpf0jj8.fra.unikraft.app
```

```text
<!doctype html>
<html lang="en">
    [...]
    <h1> Welcome to FlaskBlog </h1>

        <a href="/1">
            <h2>First Post</h2>
        </a>
        <span class="badge badge-primary">2024-02-15 22:01:07</span>
        <a href="/1/edit">
            <span class="badge badge-warning">Edit</span>
        </a>
        <hr>

        <a href="/2">
            <h2>Second Post</h2>
        </a>
</html>
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                                  STATE    IMAGE                                                    ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    httpserver-python312-flask30-sqlite-distroless-qodkd  running  <my-org>/httpserver-python312-flask30-sqlite-distroless        768MiB  1      lingering-orangutan-840mmdvd.fra....  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                                  FQDN                                  STATE    STATUS        IMAGE                                                     MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-python312-flask30-sqlite-distroless-qodkd  lingering-orangutan-840mmdvd.fra....  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-python312-flask30-sqlite-distroless@sha256...  768 MiB  1            166.25 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-python312-flask30-sqlite-distroless-qodkd
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-python312-flask30-sqlite-distroless-qodkd
```

## Implementation details

The app uses the following files:

* `schema.sql`: SQL schema for the database
* `init_db.py`: script to initialized the database file from `schema.sql` in `/app/database.db`
* `server.py` + `templates/`: the actual Flask-based implementation: Python source code file and HTML template files
* `requirements.txt`: `pip` configuration file to install required packages: Flask and SQLite
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/python3", "/app/server.py"]`: Use `/usr/bin/python3 /app/server.py` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM gcr.io/distroless/cc-debian12:latest`: Build the filesystem from the [`gcr.io/distroless/cc-debian12` container image](https://github.com/GoogleContainerTools/distroless/blob/main/cc/README.md), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY` rules copy required files.
  The process copies the `requirements.txt` file before running `pip3 install`.
  The process copies other files (including `schema.sql`, `init_db.py`) for the initialization of the database.

* `RUN` commands trigger actions such as installing Python packages and initializing the database.

* The new `gcr.io/distroless/cc-debian12` image contains the relevant contents required by the app:

  * the SQLite dynamic library: `/usr/lib/x86_64-linux-gnu/libsqlite3.so.0`
  * the Python package files: `/usr/local/lib/python3.12`
  * the `/app` directory

## Customize your app

To customize the app, update app files in the repository:

* `schema.sql`: Update the database schema.
* `server.py`, `templates/`: Update the Flask app..
* `requirements.txt`, `Dockerfile`: Update the list of Python packages used by the app.
* `Kraftfile`: Update the command line used to start the app.

The following options are available for customizing the app:

* If you only update the implementation in the `server.py` source file or `template/` directory, and the database schema in `schema.sql`, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* If you add new dependencies in `requirements.txt`, the `RUN pip3 install` in the `Dockerfile` command should take care of everything.
  It may be the case that you need to copy other files, such as the `/usr/lib/x86_64-linux-gnu/libsqlite3.so.0` for SQLite, via `COPY` commands in the `Dockerfile`.
  More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

* If you add a new Python source file that's running the `main()` function, update the `cmd` line in the `Kraftfile` and replace `server.py` to run that file when creating the instance.

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
