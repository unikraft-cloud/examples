# Flask with SQLite

This guide explains how to create and deploy a Python Flask app using SQLite.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/python3.12-flask3.0-sqlite/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/python3.12-flask3.0-sqlite/
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
kraft cloud deploy -p 443:8080 -M 512 .
```

```ansi
[●] Deployed successfully!
 │
 ├────────── name: python312-flask30-sqlite-qodkd
 ├────────── uuid: e00e7aca-962d-409c-87c2-c245ca08b54b
 ├───────── state: running
 ├─────────── url: https://lingering-orangutan-840mmdvd.fra.unikraft.app
 ├───────── image: python312-flask30-sqlite@sha256:bdb0bf35a9675b9b3836cbb626606da0606334d91768c7ba31195c3062d6f517
 ├───── boot time: 166.25 ms
 ├──────── memory: 512 MiB
 ├─────── service: lingering-orangutan-840mmdvd
 ├── private fqdn: python312-flask30-sqlite-qodkd.internal
 ├──── private ip: 172.16.3.3
 └────────── args: /usr/bin/python3 /app/server.py
```

In this case, the instance name is `python312-flask30-sqlite-qodkd` and the address is `https://lingering-orangutan-840mmdvd.fra.unikraft.app`.
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

```bash
kraft cloud instance list
```
```ansi
NAME                            FQDN                                           STATE    STATUS        IMAGE                               MEMORY   VCPUS  ARGS                             BOOT TIME
python312-flask30-sqlite-qodkd  lingering-orangutan-840mmdvd.fra.unikraft.app  running  1 minute ago  python312-flask30-sqlite@sha256...  512 MiB  1      /usr/bin/python3 /app/server.py  166250us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove python312-flask30-sqlite-qodkd
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

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: python:3.12`: The Unikraft runtime kernel to use is Python 3.12.

* `rootfs: ./Dockerfile`: Build the app root filesystem using the `Dockerfile`.

* `cmd: ["/usr/bin/python3", "/app/server.py"]`: Use `/usr/bin/python3 /app/server.py` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY` rules copy required files.
  The process copies the `requirements.txt` file before running `pip3 install`.
  The process copies other files (including `schema.sql`, `init_db.py`) for the initialization of the database.

* `RUN` commands trigger actions such as installing Python packages and initializing the database.

* The new `scratch` image contains the relevant contents required by the app:

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

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
