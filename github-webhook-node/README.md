# Webhooks: GitHub Webhook Receiver

Webhooks, also called reverse APIs, are how a service sends real-time data to other applications the moment a specific event occurs, instead of those applications polling for changes.
Events arrive in bursts and are silent in between, so a receiver that scales to zero and wakes in milliseconds costs nothing while it waits.

This example shows how to build a simple GitHub Webhook receiver using Node.js with [Express](https://expressjs.com/) and run it on Unikraft Cloud.
In this case, the webhook receiver listens for GitHub events, such as push events or pull request events, and logs them to the console.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/github-webhook-node/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/github-webhook-node/
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
unikraft build . --output <my-org>/github-webhook-node:latest
unikraft run --metro fra \
  -m 1G \
  -p 443:3000/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000,stateful=true \
  -e GITHUB_WEBHOOK_SECRET=your_secret_here \
  --image <my-org>/github-webhook-node:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 1Gi \
  -p 443:3000/tls+http \
  --scale-to-zero on \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 1s \
  -e GITHUB_WEBHOOK_SECRET=your_secret_here \
  .
```

`GITHUB_WEBHOOK_SECRET` is the secret used to verify incoming webhook requests from GitHub.
Set it to a string with high entropy.

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         github-webhook-node-bzq7u
uuid:         8a8634f1-fc78-4cc0-aa36-8f082d8a59f5
state:        starting
image:        <my-org>/github-webhook-node
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       67c7cca2-ca82-1467-e2f1-1b455edb638c
  name:       dry-cloud-uuw0qlb6
  domains:
  - fqdn:     dry-cloud-uuw0qlb6.fra.unikraft.app
networks:
- uuid:       6153b689-b713-97c3-f8bb-bd08cc47f6bc
  private-ip: 10.0.1.205
  mac:        12:b0:d0:97:b0:d2
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: github-webhook-node-bzq7u
 ├───────── uuid: 8a8634f1-fc78-4cc0-aa36-8f082d8a59f5
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://dry-cloud-uuw0qlb6.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/github-webhook-node@sha256:10974aac67ce6355148e21d91f918960bf0af29ad840fffeeb2fd01f8c905f66
 ├─────── memory: 1024 MiB
 ├────── service: dry-cloud-uuw0qlb6
 ├─ private fqdn: github-webhook-node-bzq7u.internal
 └─── private ip: 10.0.1.205
```

In this case, the instance name is `github-webhook-node-bzq7u` and the address is `https://dry-cloud-uuw0qlb6.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Node.js webhook server's health endpoint:

```bash
curl https://dry-cloud-uuw0qlb6.fra.unikraft.app/health
```

```text
{"status":"healthy","timestamp":"2025-12-17T14:55:20.953Z","uptime":0.063799807}
```

The `uptime` field is so small because Unikraft Cloud scales the instance to zero when no connections are active.
When a request comes in, Unikraft Cloud automatically starts the instance.

To see the incoming webhook events (you set up the [webhook in GitHub](#test-github-webhooks)), you can retrieve the logs of the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances logs github-webhook-node-bzq7u
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance logs github-webhook-node-bzq7u --follow
```

```console
[2025-12-17T15:20:54.524Z] Webhook received: ping
{
  "timestamp": "2025-12-17T15:20:54.524Z",
  "event": "ping",
  "data": {
    "zen": "Accessible for all.",
    ...
  },
  "receivedAt": 1765984854525
}
...
```

GitHub sends the `ping` event when you set up the webhook.
You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                       STATE    IMAGE                         ARGS  MEMORY  VCPUS  FQDN                                 CREATED
fra    github-webhook-node-bzq7u  standby  <my-org>/github-webhook-node        1.0GiB  1      dry-cloud-uuw0qlb6.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                       FQDN                                 STATE    STATUS   IMAGE                                                      MEMORY   VCPUS  ARGS  BOOT TIME
github-webhook-node-bzq7u  dry-cloud-uuw0qlb6.fra.unikraft.app  standby  standby  oci://unikraft.io/<my-org>/github-webhook-node@sha256:...  1.0 GiB  1            197.47 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete github-webhook-node-bzq7u
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove github-webhook-node-bzq7u
```

## Test GitHub webhooks

To test the GitHub webhook receiver, you must set up a [webhook in a GitHub repository](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks).
Make sure to set the payload address to the Unikraft Cloud instance webhook, in this case `https://dry-cloud-uuw0qlb6.fra.unikraft.app/webhook/github`.
You should also set the content type to `application/json` and select the events you want to receive.
Lastly, you should set the secret to verify that the requests come from GitHub and weren't tampered with.
Now, once you make changes in the repository (that you are listening to), you should see the webhook events logged in the instance logs:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances logs github-webhook-node-bzq7u
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance logs github-webhook-node-bzq7u --follow
```

```console
[2025-12-17T17:28:51.136Z] Webhook received: push
{
  "timestamp": "2025-12-17T17:28:51.136Z",
  "event": "push",
  "data": {
    "ref": "refs/heads/main",
    "before": "3312f99896b85e896f730d246180979553748f9d",
    "after": "12b2962bbc70f92fa33e4b30c0e1a3ed5f35f9d4",
    "repository": {
      "id": 123456789,
      "name": "your-repo",
      ...
    },
    ...
  },
  "receivedAt": 1765992531136
}
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `server.js`: The Node.js Express web server that handles GitHub webhook events
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

## Learn more

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
