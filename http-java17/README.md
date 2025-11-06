# Java

This guide explains how to create and deploy a simple Java-based HTTP web server.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-java17/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-java17/
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

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: http-java17-xx739
 ├────────── uuid: 15346dbe-6c6e-461a-a998-e6fc9bfa6d89
 ├───────── state: running
 ├─────────── url: https://bold-voice-irwjijr5.fra.unikraft.app
 ├───────── image: http-java17@sha256:554deac043859fc0eb4f8aeebe2daeb76c5d30960157a00746b9fb7b177ef0ca
 ├───── boot time: 157.15 ms
 ├──────── memory: 1024 MiB
 ├─────── service: bold-voice-irwjijr5
 ├── private fqdn: http-java17-xx739.internal
 ├──── private ip: 172.16.28.2
 └────────── args: /usr/lib/jvm/java-17-openjdk-amd64/bin/java -classpath /usr/src/ SimpleHttpServer
```

In this case, the instance name is `http-java17-xx739` and the address is `https://bold-voice-irwjijr5.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Java-based HTTP web server:

```bash
curl https://bold-voice-irwjijr5.fra.unikraft.app
```
```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```
```ansi
NAME               FQDN                                  STATE    STATUS        IMAGE                                                 MEMORY   VCPUS  ARGS                             BOOT TIME
http-java17-xx739  bold-voice-irwjijr5.fra.unikraft.app  running  1 minute ago  http-java17@sha256:6f4cb7632ecbab952feb072e37a1a9...  1.0 GiB  1      /usr/lib/jvm/java-17-openjdk...  157154us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-java17-xx739
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `SimpleHttpServer.java`: the actual Java HTTP server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: java:latest`: The Unikraft runtime kernel to use is Java.

* `rootfs: ./Dockerfile`: Build the app root filesystem using the `Dockerfile`.

* `cmd:`: Use as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY ./SimpleHttpServer.java /src/SimpleHttpServer.java`: Copy the server implementation file in the Docker filesystem.

* `RUN javac SimpleHttpServer.java`: Compile the Java source file.

The following options are available for customizing the app:

* If you only update the implementation in the `SimpleHttpServer.java` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
