# Sandboxes: OpenClaw

Sandboxes are on-demand, isolated execution environments for work you would rather not run next to anything else, such as AI agent tool calls, user-submitted code, or third-party plugins.
This example uses [OpenClaw](https://openclaw.ai/), an autonomous AI agent framework, as the sandboxed workload: the gateway and everything the agent runs stay inside a dedicated microVM, which scales to zero when idle and resumes in milliseconds.

This guide explains how to create and deploy your very own OpenClaw gateway on Unikraft Cloud.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/openclaw` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/openclaw/
   ```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
unikraft login
```

When done, you may create the OpenClaw Unikraft Cloud image and deploy an instance from it like so:

```bash
unikraft build . --output <my-org>/openclaw:latest
unikraft run --metro fra \
  -m 4G \
  -p 18789:18789/tls \
  -p 2222:2222/tls \
  --scale-to-zero policy=on,cooldown-time=10000,stateful=true \
  -e PUBKEY="...." \
  --image <my-org>/openclaw:latest
```

Make sure to replace `<my-org>` with your username / org-name and to set your SSH public key as the `PUBKEY` environment variable above.

The output shows the instance address and other details:

```ansi
metro:        fra
name:         openclaw-8tosm
uuid:         e2a6183a-721b-4145-bfaf-37a5f859bbc1
state:        running
image:        <my-org>/openclaw
runtime:
  env:
    PUBKEY:   *
resources:
  memory:     4GiB
  vcpus:      1
service:
  uuid:       7ab20338-b04d-4869-947b-9433e21677b1
  name:       divine-flower-bxsaapup
  domains:
  - fqdn:     divine-flower-bxsaapup.fra.unikraft.app
networks:
- uuid:       2b0b120b-6ce5-4b19-ac4c-04ee8f11526e
  private-ip: 10.0.12.97
  mac:        12:b0:0a:00:0c:61
timestamps:
  created:    just now
```

In this case, the instance name is `openclaw-8tosm` and the address is `divine-flower-bxsaapup.fra.unikraft.app`.
These will be different for each run.

You can now SSH into this instance and run the OpenClaw onboarding process.

In order to SSH, you need to set up a tunnel that handles the TLS connection to the Unikraft Cloud instance.
This way, you have a non-TLS port that your SSH client can connect to:

```bash
socat TCP-LISTEN:2222,reuseaddr,fork OPENSSL:divine-flower-bxsaapup.fra.unikraft.app:2222,verify=0
```

Then connect to the instance via SSH using:

```bash
ssh -l root localhost -p 2222
```

You can list information about the instance by running:

```bash
unikraft instances list
```

```ansi
METRO  NAME            STATE    IMAGE                     ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    openclaw-8tosm  running  <my-org>/openclaw:latest        4GiB    1      divine-flower-bxsaapup.fra.unikraft.app  2 minutes ago
```

When done, you can remove the instance using:

```bash
unikraft instances delete openclaw-8tosm
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
unikraft --help
```

## OpenClaw Setup

Once you have SSH'd into your instance, you may run:

```bash
openclaw onboard
```

This will set up your OpenClaw gateway on the instance.
You will be asked to provide your LLM's API key here.

Once done, make note of your `gateway.auth.token` (henceforth referenced as `<token>`) from `~/.openclaw/openclaw.json`

```bash
cat ~/.openclaw/openclaw.json
```

Set `gateway.controlUi.allowedOrigins` in `~/.openclaw/openclaw.json`:

```json
...
  "gateway": {
    ...
    "controlUi": {
      "allowedOrigins": [
        "https://proud-smoke-cjf0wro8.fra.unikraft.app:18789"
      ]
    },
    ...
  },
...
```

Replace the domain in the above URL with the address of your instance (noted earlier).

Run the gateway:

```bash
openclaw gateway run --bind lan
```

You may now access the web dashboard using the following URL:

```ansi
https://<address>:18789?token=<token>
```

Where `<address>` is your above noted address and `<token>` is your above noted token.

For security reasons, you will have to manually approve your web "device" in order to start using the web dashboard.
Create a new SSH connection to your OpenClaw instance:

```bash
ssh -l root localhost -p 2222
```

First, find your device ID:

```bash
openclaw devices list
```

Look under the `Request` column.
Device IDs look like `cabd915e-137a-4bc4-b640-d0e507684d65`

Finally, approve your device with:

```bash
openclaw devices approve <device-id>
```

Once this is done, refresh your OpenClaw web dashboard.

You now have full access to your very own OpenClaw deployment on Unikraft Cloud!
