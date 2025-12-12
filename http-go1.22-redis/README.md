# Go with Redis

This guide explains how to create and deploy a Go app with a Redis database.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/http-go1.22-redis` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/http-go1.22-redis/
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
kraft cloud compose up
```

The output shows the instance address and other details.
To set a value in Redis via the Go server, invoke:

```bash
curl -X POST -d "key=my-key" -d "value=my-value" https://<FQDN>
```

You can then retrieve the value by accessing the path:

```bash
curl https://<FQDN>/?key=my-key
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
