# Java HTTP Server

This is a simple HTTP server written in the [Java](https://www.java.com/en/) programming language.

To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-java21` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-java21/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-java21:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-java21:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-java21-5xw9m
uuid:         b2c3d4e5-f6a7-8901-bcde-f12345678901
state:        starting
image:        <my-org>/httpserver-java21
resources:
  memory:     1GiB
  vcpus:      1
service:
  uuid:       9d96e042-1601-352b-10c7-4a8c7ececbcb
  name:       gentle-wind-b2x9pkqm
  domains:
  - fqdn:     gentle-wind-b2x9pkqm.fra.unikraft.app
networks:
- uuid:       25185154-a4d5-0da1-e28f-3b3e42190b56
  private-ip: 10.0.3.5
  mac:        12:b0:29:0f:68:f3
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-java21-5xw9m` and the address is `https://gentle-wind-b2x9pkqm.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Java HTTP server:

```bash
curl https://gentle-wind-b2x9pkqm.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                     STATE    IMAGE                       ARGS  MEMORY  VCPUS  FQDN                              CREATED
fra    httpserver-java21-5xw9m  running  <my-org>/httpserver-java21        1GiB    1      gentle-wind-b2x9pkqm.fra.unik...  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-java21-5xw9m
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem
* `SimpleHttpServer.java`: the Java HTTP server implementation

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/opt/java/openjdk/bin/java", "-classpath", "/usr/src/", "SimpleHttpServer"]`: Use the Java runtime to run `SimpleHttpServer` as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM --platform=$BUILDPLATFORM eclipse-temurin:21-jdk-noble AS build`: Build the app with the Eclipse Temurin 21 JDK on the build machine.
  The Java class file does not depend on the architecture.

* `RUN javac SimpleHttpServer.java`: Compile the Java source file.

* `FROM eclipse-temurin:21-jre-noble AS runtime`: Use the Eclipse Temurin 21 JRE for the target architecture.

* `RUN ... lddtree ...`: Collect the JRE, the system libraries that it uses, and the compiled `SimpleHttpServer.class` in `/rootfs`.

* `FROM scratch`: Build the runtime filesystem from a minimal base image.

* `COPY --from=runtime /rootfs /`: Copy the collected files to the app filesystem.

The following options are available for customizing the app:

* If you only update the implementation in the `SimpleHttpServer.java` source file, you don't need to make any other changes.

* If you want to add extra files, copy them to `/rootfs` in the `runtime` stage with a `COPY` command in the `Dockerfile`.
  Only the contents of `/rootfs` go into the final image.

* If you want to replace `SimpleHttpServer.java` with a different source file, update the `cmd` line in the `Kraftfile` and replace `SimpleHttpServer` with the name of your new class.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

- [Java's Documentation](https://docs.oracle.com/en/java/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)


Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
