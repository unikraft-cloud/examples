# Spring Boot HTTP Server (Distroless)

This guide explains how to create and deploy a Spring Boot web server, using a [distroless](https://github.com/GoogleContainerTools/distroless) base image (`gcr.io/distroless/java17-debian13`) for the runtime stage instead of a manually assembled `scratch` image.

This example is a variant of [`httpserver-java17-springboot`](../httpserver-java17-springboot).

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-java17-springboot-distroless/` directory:

```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-java17-springboot-distroless/
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
unikraft build . --output <my-org>/httpserver-java17-springboot-distroless:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-java17-springboot-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 1Gi \
  -p 443:8080/tls+http \
  --scale-to-zero idle \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-java17-springboot-distroless-qseeo
uuid:         b081166d-a2a0-43af-982d-1aa17f06b5c4
state:        starting
image:        <my-org>/httpserver-java17-springboot-distroless
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

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-java17-springboot-distroless-qseeo
 ├───────── uuid: b081166d-a2a0-43af-982d-1aa17f06b5c4
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://long-dust-si7xsngk.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-java17-springboot-distroless@sha256:cc2f2ad18ce8e36b8e8f4debee096fef7b0bb8b47762575a2ba5a9de8199c64a
 ├─────── memory: 1024 MiB
 ├────── service: long-dust-si7xsngk
 ├─ private fqdn: httpserver-java17-springboot-distroless-qseeo.internal
 └─── private ip: 10.0.6.2
```

In this case, the instance name is `httpserver-java17-springboot-distroless-qseeo` and the address is `https://long-dust-si7xsngk.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Spring Boot server's `hello` endpoint:

```bash
curl https://long-dust-si7xsngk.fra.unikraft.app/hello
```

```text
Hello World!
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-java17-springboot-distroless-qseeo
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-java17-springboot-distroless-qseeo
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

* `cmd: ["/usr/bin/java", "-jar", "/usr/src/demo-0.0.1-SNAPSHOT.jar"]`: Use the Java runtime to run the Spring Boot JAR as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM --platform=linux/x86_64 debian:bookworm AS build`: Build the app using Debian Bookworm, installing the JDK and Maven tooling needed to generate and compile the Spring Boot project.

* `RUN curl -G https://start.spring.io/starter.zip ...`: Generate the Spring Boot project skeleton via Spring Initializr.

* `COPY DemoApplication.java src/main/java/com/example/demo/`: Copy the server implementation file into the generated project.

* `RUN ./mvnw compile package install`: Build the Spring Boot JAR.

* `FROM gcr.io/distroless/java17-debian13`: Build the runtime filesystem from Google's [distroless](https://github.com/GoogleContainerTools/distroless) Java 17 base image, which already contains a minimal JRE and its required system libraries, instead of manually copying individual files into a `scratch` image.

* `COPY --from=build /src/target/demo-0.0.1-SNAPSHOT.jar /usr/src/demo-0.0.1-SNAPSHOT.jar`: Copy the compiled JAR into the app filesystem.

The following options are available for customizing the app:

* If you only update the implementation in the `DemoApplication.java` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                               STATE    IMAGE                                             ARGS  MEMORY   VCPUS  FQDN                                 CREATED
fra    httpserver-java17-springboot-distroless-qseeo      running  <my-org>/httpserver-java17-springboot-distroless        1024MiB  1      long-dust-si7xsngk.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                               FQDN                                 STATE    STATUS        IMAGE                                                                              MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-java17-springboot-distroless-qseeo      long-dust-si7xsngk.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-java17-springboot-distroless@sha256:...     1.0 GiB  1            421.30 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-java17-springboot-distroless-qseeo
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-java17-springboot-distroless-qseeo
```

## Learn more

- [Spring Boot Documentation](https://docs.spring.io/spring-boot/index.html)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)

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
