# C

This guide explains how to create and deploy a C app.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-c` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-c/
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
kraft cloud deploy -p 443:8080 .
```

The output shows the instance address and other details:

```ansi
[●] Deployed successfully!
 │
 ├────── name: http-c-is2s9
 ├────── uuid: bec814ce-6ed5-4858-b247-e7f0b17750f5
 ├───── metro: https://api.fra.unikraft.cloud/v1
 ├───── state: running
 ├──── domain: https://still-resonance-bja3lste.fra.unikraft.app
 ├───── image: http-c@sha256:375677bf052f14c18ca79c86d2f47a68f3ea5f8636bcd8830753a254f0e06c1b 
 ├─ boot time: 13.29 ms
 ├──── memory: 128 MiB
 ├─── service: still-resonance-bja3lste
 ├ private ip: 10.0.0.49
 └────── args: /http_server
```

In this case, the instance name is `http-c-is2s9` and the address is `https://still-resonance-bja3lste.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance:

```bash
curl https://still-resonance-bja3lste.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

```bash
kraft cloud instance list
```

```ansi
NAME          FQDN                                       STATE    STATUS   IMAGE                                     MEMORY   VCPUS  ARGS          BOOT TIME
http-c-is2s9  still-resonance-bja3lste.fra.unikraft.app  standby  standby  http-c@sha256:375677bf052f14c18ca79c8...  128 MiB  1      /http_server  12.91 ms
```

When done, you can remove the instance:

```bash
kraft cloud instance remove http-c-is2s9
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
