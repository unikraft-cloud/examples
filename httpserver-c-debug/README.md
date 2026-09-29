# SSH and HTTP Server with C and Debugging Tools

This guide explains how to create and deploy a C app with debugging enabled.
To run this example, follow these steps:

1. Install the [unikraft CLI](https://unikraft.com/docs/cli).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-c-debug` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-c-debug/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

For extensive debug information with `strace`, add the `USE_STRACE=1` environment variable to the deploy command:

```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-c-debug:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  -p 2222:2222/tls \
  --scale-to-zero policy=off \
  -e PUBKEY=.... \
  -e USE_STRACE=1 \
  --image <my-org>/httpserver-c-debug:latest
```

The output shows the instance address and other details:

```ansi title="unikraft"
metro:        fra
name:         httpserver-c-debug-5pvem
uuid:         08629a94-e2b1-466e-abb9-15ce46411b66
state:        starting
image:        <my-org>/httpserver-c-debug
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       2e016406-0c59-4d74-6deb-fdcb206fdb1e
  name:       patient-snow-zdzhdy8r
  domains:
  - fqdn:     patient-snow-zdzhdy8r.fra.unikraft.app
networks:
- uuid:       80a11393-8eca-ec11-3028-fb8908b21894
  private-ip: 10.0.0.109
  mac:        12:b0:45:b3:18:b2
timestamps:
  created:    just now
```

In this case, the instance name is `httpserver-c-debug-5pvem` and the address is `patient-snow-zdzhdy8r.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance:

```bash
curl https://patient-snow-zdzhdy8r.fra.unikraft.app
```

```text
Hello, World!
```

For SSH, you need to set up a tunnel that handles the TLS connection to the Unikraft Cloud instance.
This way, you have a non-TLS port that your SSH client can connect to:

```bash
socat TCP-LISTEN:2222,reuseaddr,fork OPENSSL:patient-snow-zdzhdy8r.fra.unikraft.app:2222,verify=0
```

Then connect to the instance via SSH using:

```bash
ssh -l root localhost -p 2222
```

You might see warnings like `REMOTE HOST IDENTIFICATION HAS CHANGED`.
This is normal if you have set up tunnels to connect with SSH on `localhost`, so don't worry.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                      STATE    IMAGE                        ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    httpserver-c-debug-5pvem  running  <my-org>/httpserver-c-debug        256MiB  1      patient-snow-zdzhdy8r.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete httpserver-c-debug-5pvem
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft).
