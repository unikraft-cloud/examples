# Spring Boot HTTP Server

This guide explains how to create and deploy a Spring Boot web server.
To run this example, follow these steps:

1. Install the CLI and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-java17-springboot3.5.x/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-java17-springboot3.5.x/
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
unikraft build . --output <my-org>/httpserver-java17-springboot3.5.x:latest
unikraft run --metro fra -p 443:8080/tls+http -m 1G --image <my-org>/httpserver-java17-springboot3.5.x:latest
```

or

```bash title="kraft"
kraft cloud deploy -p 443:8080/tls+http -M 1G .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────────── name: httpserver-java17-springboot32x-qseeo
 ├────────── uuid: b081166d-a2a0-43af-982d-1aa17f06b5c4
 ├───────── state: running
 ├─────────── url: https://long-dust-si7xsngk.fra.unikraft.app
 ├───────── image: httpserver-java17-springboot32x@sha256:cc2f2ad18ce8e36b8e8f4debee096fef7b0bb8b47762575a2ba5a9de8199c64a
 ├───── boot time: 153.97 ms
 ├──────── memory: 1024 MiB
 ├─────── service: long-dust-si7xsngk
 ├── private fqdn: httpserver-java17-springboot32x-qseeo.internal
 ├──── private ip: 172.16.6.2
 └────────── args: /usr/lib/jvm/java-17-openjdk-amd64/bin/java -jar /usr/src/demo-0.0.1-SNAPSHOT.jar
```

In this case, the instance name is `httpserver-java17-springboot32x-qseeo` and the address is `https://long-dust-si7xsngk.fra.unikraft.app`.
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
unikraft instances delete httpserver-java17-springboot32x-qseeo
```

or

```bash title="kraft"
kraft cloud instance remove httpserver-java17-springboot32x-qseeo
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `DemoApplication.java`: the server
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.6`: The current `Kraftfile` specification version is `0.6`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `type: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

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

or

```bash title="kraft"
kraft cloud instance list
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-java17-springboot32x-qseeo
```

or

```bash title="kraft"
kraft cloud instance remove httpserver-java17-springboot32x-qseeo
```


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
