# Rust with Scale-to-Zero

This guide explains how to create and deploy a Rust app with scale-to-zero enabled.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-rust-1.79-axum-scale-to-zero` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-rust-1.79-axum-scale-to-zero/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy the app on Unikraft Cloud:

```bash
kraft cloud deploy --scale-to-zero on -p 443:8080 -M 512 .
```

Alternatively, you can expose the application with the non-HTTP mode by using a different port:

```bash
kraft cloud deploy --scale-to-zero on -p 8080:8080/tls -M 512 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────── name: http-rust-179-axum-scale-to-zero-5vhoh
 ├────── uuid: 9bb36cb4-11e4-4ab5-ba20-cb0c29571e90
 ├───── metro: https://api.fra.unikraft.cloud/v1
 ├───── state: running
 ├──── domain: https://icy-butterfly-ygnprvel.fra.unikraft.app
 ├───── image: http-rust-179-axum-scale-to-zero@sha256:08b0a4d7237e3ca40166ae57c22b3f99befa2530e4696a97c0c47c3f81345c89 
 ├─ boot time: 14.29 ms
 ├──── memory: 512 MiB
 ├─── service: icy-butterfly-ygnprvel
 ├ private ip: 10.0.0.49
 └────── args: /server
```

In this case, the instance name is `http-rust-179-axum-scale-to-zero-5vhoh` and the address is `https://icy-butterfly-ygnprvel.fra.unikraft.app`.
They're different for each run.

This mode allows you to use more advanced HTTP features such as [Server-Sent-Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events).

After deploying, you can interact with the following endpoints:

| Endpoint | Description | Curl Example |
| -------- | ----------- | ------------ |
| `GET` `<URL>/` | Get the current content of the `scale_to_zero_disable` file | `curl https://<FQDN>/` |
| `POST` `<URL>/set/<number>` | Set the count of disable requests to `<number>` | `curl -X POST https://<FQDN>/set/10` |
| `POST` `<URL>/add` | Increment the count by one | `curl -X POST https://<FQDN>/add` |
| `POST` `<URL>/add/<number>` | Increment the count by `<number>` | `curl -X POST https://<FQDN>/add/2` |
| `POST` `<URL>/sub` | Decrement the count by one | `curl -X POST https://<FQDN>/sub` |
| `POST` `<URL>/sub/<number>` | Decrement the count by `<number>` | `curl -X POST https://<FQDN>/sub/2` |
| `GET` `<URL>/sse/<interval>` | Get periodic server side events every `<interval>` seconds (Only works for a non-HTTP handler port) | `curl https://<FQDN>/sse/1` |

You can list information about the instance by running:

```bash
kraft cloud instance list
```

```ansi
NAME                                    FQDN                                     STATE    STATUS        IMAGE                                         MEMORY   VCPUS  ARGS     BOOT TIME
http-rust-179-axum-scale-to-zero-5vhoh  icy-butterfly-ygnprvel.fra.unikraft.app  running  1 minute ago  http-rust-179-axum-scale-to-zero@sha256:0...  512 MiB  1      /server  14291us
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-cpp-boost-rae7s
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
