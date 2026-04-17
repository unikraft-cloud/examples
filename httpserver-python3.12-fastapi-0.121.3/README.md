# FastAPI HTTP Server

This guide explains how to create and deploy a Python FastAPI web app.
To run this example, follow these steps:

1. Install the CLI and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).

1. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-python3.12-fastapi-0.121.3/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-python3.12-fastapi-0.121.3/
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

or

```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-python3.12-fastapi-0.121.3:latest
unikraft run --metro fra -p 443:8080/tls+http -m 512M --image <my-org>/httpserver-python3.12-fastapi-0.121.3:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:8080/tls+http -M 512M .
```

The output shows the instance address and other details:

```text
[●] Deployed successfully!
 │
 ├────── name: httpserver-python312-fastapi-01213-0n84f
 ├────── uuid: 5d7fc331-3c23-4953-b025-d152a872ea29
 ├───── metro: fra
 ├───── state: running
 ├──── domain: https://dry-water-0oexx89g.fra.unikraft.app
 ├───── image: httpserver-python312-fastapi-01213@sha256:fb2a00dcf1cfc3ac821cbda05f82f38d66e63121344b9bc60c6a6e2f11917b98
 ├─ boot time: 170.42 ms
 ├──── memory: 512 MiB
 ├─── service: dry-water-0oexx89g
 ├ private ip: 10.0.1.69
 └────── args: /usr/bin/python3 -m uvicorn src.server:app --host 0.0.0.0 --port 8080
```

In this case, the instance name is `httpserver-python312-fastapi-01213-0n84f` and the address is `https://dry-water-0oexx89g.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Python FastAPI web app server:

```bash
curl https://dry-water-0oexx89g.fra.unikraft.app
```

```text
{"Hello":"World"}
```
You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

or

```bash title="kraft"
kraft cloud instance list
```

```ansi
NAME                                      FQDN                                 STATE    STATUS   IMAGE                                        MEMORY   VCPUS  ARGS                                                 BOOT TIME
httpserver-python312-fastapi-01213-0n84f  dry-water-0oexx89g.fra.unikraft.app  standby  standby  httpserver-python312-fastapi-01213@sha25...  512 MiB  1      /usr/bin/python3 -m uvicorn src.server:app --hos...  169.45 ms
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances remove httpserver-python312-fastapi-01213-0n84f
```

or

```bash title="kraft"
kraft cloud instance remove httpserver-python312-fastapi-01213-0n84f
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.py`: the entry point for the app
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base-compat:latest`: The Unikraft runtime kernel to use is the latest that provides a minimal Linux-compatible environment.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `type: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/python3", "-m", "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080"]`: Use this as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

The following options are available for customizing the app:

* If you only update the implementation in the `server.py` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).
  This includes the use of Python frameworks and the use of `pip`, as shown in the next section.

## Using `pip`

[`pip`](https://pip.pypa.io/en/stable/) is a package manager for Python.
It's used to install dependencies for Python apps.
`pip` uses the `requirements.txt` file to list required dependencies (with versions).

The [`httpserver-python3.12-fastapi-0.121.3`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-python3.12-fastapi-0.121.3) guide details the use of `pip` to deploy an app using the [`FastAPI`](https://fastapi.tiangolo.com/) framework on Unikraft Cloud.

Run the command below to deploy the app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-python3.12-fastapi-0.121.3:latest
unikraft run --metro fra -p 443:8080/tls+http -m 512M --image <my-org>/httpserver-python3.12-fastapi-0.121.3:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:8080/tls+http -M 512M .
```

Differences from the FastAPI app are also the steps required to create an `pip`-based app:

1. Add the `requirements.txt` file used by `pip`.

2. Add framework-specific source files.
   In this case, this means the `server.py` file.

3. Update the `Dockerfile` to:

   3.1. `COPY` the local files.

   3.2. `RUN` the `pip3 install` command to install dependencies.

   3.3. `COPY` of the resulting and required files (`/usr/local/lib/python3.12` and `server.py`) in the app filesystem, using the [`scratch` container](https://hub.docker.com/_/scratch/).

The following lists the files:

The `requirements.txt` file lists the `fastapi` and `uvicorn` dependencies.

The `Kraftfile` is the same one used for `httpserver-python3.12`, except changed lines that have the following roles:
* `cmd: ["/usr/bin/python3", "-m", "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080"]`: Use `/usr/bin/python3 -m uvicorn src.server:app --host 0.0.0.0 --port 8080` as the starting command of the instance.

For `Dockerfile` newly added lines have the following roles:

* `FROM python:3.12-bookworm AS build`: Use the base image of the `python:3.12-bookworm` container.
  This provides the `pip3` binary and other Python-related components.
  Name the current image `build`.

* `WORKDIR /app`: Use `/app` as working directory.
  All other commands in the `Dockerfile` run inside this directory.

* `COPY requirements.txt /app`: Copy the package configuration file to the Docker filesystem.

* `RUN pip3 install ...`: Install `pip` components listed in `requirements.txt`.

* `COPY --from=build ...`: Copy generated Python files in the new `build` image in the `scratch`-based image.

Similar actions apply to other `pip3`-based apps.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

or

```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
