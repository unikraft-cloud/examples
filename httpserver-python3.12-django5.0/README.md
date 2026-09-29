# Django HTTP Server

This guide explains how to create and deploy a Python Django web app.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-python3.12-django5.0/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-python3.12-django5.0/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-python312-django50:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:80/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-python312-django50:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-python312-django50-vt56c
uuid:         d8469447-fdf6-4caf-9fea-494218ca6f72
state:        starting
image:        <my-org>/httpserver-python312-django50
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       109aa11f-da45-8d57-d5e4-6eb509ee3e73
  name:       dawn-sound-n5wrkxi2
  domains:
  - fqdn:     dawn-sound-n5wrkxi2.fra.unikraft.app
networks:
- uuid:       95f37ba4-2586-54a2-bf3e-5764c91c4fc1
  private-ip: 10.0.6.5
  mac:        12:b0:9c:af:65:e7
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-python312-django50-vt56c` and the address is `https://dawn-sound-n5wrkxi2.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Django web app server:

```bash
curl https://dawn-sound-n5wrkxi2.fra.unikraft.app
```

```html

<!doctype html>

<html lang="en-us" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>The install worked successfully! Congratulations!</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          html {
            line-height: 1.15;
          }
          a {
            color: #19865C;
          }
[...]
```

Or point a browser at the address and/or its `/admin` area.
You can set the username and password in the `Dockerfile` (more on this file later) to `unikraft/unikraft`.

> **Caution:**
> The example sets ALLOWED_HOSTS to * and runs in debug mode.
> For a production site, ensure you read the recommended deployment guides of the official Django project.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                 STATE    IMAGE                                   ARGS  MEMORY   VCPUS  FQDN                                  CREATED
fra    httpserver-python312-django50-vt56c  running  <my-org>/httpserver-python312-django50        1024MiB  1      dawn-sound-n5wrkxi2.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances remove httpserver-python312-django50-vt56c
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `main.py`: the entry point for the app
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/python3", "/app/main.py"]`: Use this as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

The following options are available for customizing the app:

* If you only update the implementation in the `main.py` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).
  This includes the use of Python frameworks and the use of `pip`, as shown in the next section.

## Using `pip`

[`pip`](https://pip.pypa.io/en/stable/) is a package manager for Python.
It's used to install dependencies for Python apps.
`pip` uses the `requirements.txt` file to list required dependencies (with versions).

The [`httpserver-python3.12-flask3.0`](https://github.com/unikraft-cloud/examples/tree/main/httpserver-python3.12-flask3.0) guide details the use of `pip` to deploy an app using the [`Flask`](https://flask.palletsprojects.com/en/3.0.x/) framework on Unikraft Cloud.

Run the command below to deploy the app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-python312-flask30:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:80/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-python312-flask30:latest
```

Differences from the Django app are also the steps required to create an `pip`-based app:

1. Add the `requirements.txt` file used by `pip`.

2. Add framework-specific source files.
   In this case, this means the `server.py` file.

3. Update the `Dockerfile` to:

   3.1. `COPY` the local files.

   3.2. `RUN` the `pip3 install` command to install dependencies.

   3.3. `COPY` of the resulting and required files (`/usr/local/lib/python3.12` and `server.py`) in the app filesystem, using the [`scratch` container](https://hub.docker.com/_/scratch/).

The following lists the files:

The `requirements.txt` file lists the `flask` dependency.

The `Kraftfile` is the same one used for Django.

For `Dockerfile` newly added lines have the following roles:

* `FROM python:3.12-bookworm AS base`: Use the base image of the `python:3.12-bookworm` container.
  This provides the `pip3` binary and other Python-related components.
  Name the current image `base`.

* `WORKDIR /app`: Use `/app` as working directory.
  All other commands in the `Dockerfile` run inside this directory.

* `COPY requirements.txt /app`: Copy the package configuration file to the Docker filesystem.

* `RUN pip3 install ...`: Install `pip` components listed in `requirements.txt`.

* `COPY --from=base ...`: Copy generated Python files in the new `base` image in the `scratch`-based image.

Similar actions apply to other `pip3`-based apps.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
