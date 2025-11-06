# Wordpress with Nginx and MariaDB

This guide explains how to create and deploy a Wordpress app with Nginx and MariaDB.
To run this example, follow these steps:

1. Install the [`kraft` CLI tool](https://unikraft.org/docs/cli/install) and a container runtime engine, for example [Docker](https://docs.docker.com/engine/install/).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/wordpress-compose` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/wordpress-compose/
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
kraft cloud compose up -d
```

The Wordpress server is exposed through Nginx. To get the public URL of the deployed application, run:

```bash
kraft cloud instance get wordpress-compose-wordpress
```

and look for the `fqdn` field in the output.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
