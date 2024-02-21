# Python Django web application

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Then, clone this repository and `cd` into this directory.
To deploy this application on KraftCloud, invoke:

```console
kraft cloud deploy -M 512 -p 443:80 .
```

## Important notes

The example sets ALLOWED_HOSTS to `*` and runs in debug mode. For a production site read the deployment guides of the Django project carefully.

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
