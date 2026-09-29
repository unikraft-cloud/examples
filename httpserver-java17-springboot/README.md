# Spring Boot HTTP Server

This guide explains how to create and deploy a Spring Boot web server.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-java17-springboot/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-java17-springboot/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-java17-springboot:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-java17-springboot:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-java17-springboot-qseeo
uuid:         b081166d-a2a0-43af-982d-1aa17f06b5c4
state:        starting
image:        <my-org>/httpserver-java17-springboot
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       04f5b3ce-0aae-a50a-9d58-e6fa618b2cdc
  name:       long-dust-si7xsngk
  domains:
  - fqdn:     long-dust-si7xsngk.fra.unikraft.app
networks:
- uuid:       4bde3abf-faf8-3a14-ceb9-bc05e646dfac
  private-ip: 10.0.6.2
  mac:        12:b0:eb:ad:60:a2
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-java17-springboot-qseeo` and the address is `https://long-dust-si7xsngk.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Spring Boot server's `hello` endpoint:

```bash
curl https://long-dust-si7xsngk.fra.unikraft.app/hello
```

```text
Hello World!
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-java17-springboot-qseeo
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `DemoApplication.java`: the server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/lib/jvm/java-17-openjdk-amd64/bin/java", "-jar", "/usr/src/demo-0.0.1-SNAPSHOT.jar"]`: Use as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY DemoApplication.java src/main/java/com/example/demo/`: Copy the server implementation file in the Docker filesystem.

The following options are available for customizing the app:

* If you only update the implementation in the `DemoApplication.java` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                   STATE    IMAGE                                     ARGS  MEMORY   VCPUS  FQDN                                 CREATED
fra    httpserver-java17-springboot-qseeo     running  <my-org>/httpserver-java17-springboot           1024MiB  1      long-dust-si7xsngk.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-java17-springboot-qseeo
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
