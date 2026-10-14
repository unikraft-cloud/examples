# Spring PetClinic (Distroless)

[Spring PetClinic](https://github.com/spring-projects/spring-petclinic) is an example project that uses Spring Boot to model a simple pet clinic, built here using a [distroless](https://github.com/GoogleContainerTools/distroless) base image (`gcr.io/distroless/java17-debian13`) for the runtime stage instead of a manually assembled `scratch` image.

This example is a variant of [`httpserver-java17-spring-petclinic`](../httpserver-java17-spring-petclinic).

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-java17-spring-petclinic-distroless/` directory:

```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-java17-spring-petclinic-distroless/
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
unikraft build . --output <my-org>/httpserver-java17-spring-petclinic-distroless:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:8080/tls+http \
  --scale-to-zero policy=idle,cooldown-time=1000,stateful=true \
  --image <my-org>/httpserver-java17-spring-petclinic-distroless:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --metro fra \
  -M 1Gi \
  -p 443:8080/tls+http \
  --scale-to-zero idle \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  .
```

In this case, the instance name and address are printed in the output, and differ for each run.

After deploying, point your browser to the provided URL.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete <instance-name>
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove <instance-name>
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd: ["/usr/bin/java", "-jar", "/usr/src/spring-petclinic-3.3.0-SNAPSHOT.jar"]`: Use the Java runtime to run the PetClinic JAR as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM --platform=linux/x86_64 debian:bookworm AS build`: Build the app using Debian Bookworm, installing the JDK and Git tooling needed to fetch and compile the project.

* `RUN git clone https://github.com/spring-projects/spring-petclinic.git /src`: Fetch the Spring PetClinic source code.

* `RUN git checkout -b build ${BUILD_COMMIT}`: Pin the build to a specific, known-good commit, so the build is reproducible even if the upstream project changes.

* `RUN --mount=type=cache,target=/root/.m2 ./mvnw package`: Compile the project and package it as a runnable JAR, using a cache mount to speed up repeated builds.

* `FROM gcr.io/distroless/java17-debian13`: Build the runtime filesystem from Google's [distroless](https://github.com/GoogleContainerTools/distroless) Java 17 base image, which already contains a minimal JRE and its required system libraries, instead of manually copying individual files into a `scratch` image.

* `COPY --from=build /src/target/spring-petclinic-3.3.0-SNAPSHOT.jar /usr/src/spring-petclinic-3.3.0-SNAPSHOT.jar`: Copy the compiled JAR into the app filesystem.

To use a different upstream commit or version of Spring PetClinic, update the `BUILD_COMMIT` build argument in the `Dockerfile`.

## Learn more

- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
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
